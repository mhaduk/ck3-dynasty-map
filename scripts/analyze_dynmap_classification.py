#!/usr/bin/env python3
"""Offline V1/V2/V3 history plus build-bound V4 native-counter audit.

Exit 0: complete emitted roster/records, all independently verified roles/RGBs
match. Exit 1: complete evidence with a semantic or intended-RGB mismatch.
Exit 2: incomplete/unverified/unavailable evidence or input/output error.
No exit code verifies stored RGB, pixels, CK3 parsing, or iterator coverage.
"""

import argparse
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


PREFIX = "DYNMAP_R016 AUDIT V1 "
BEGIN = "BATCH_BEGIN SOURCE F001_DUMP_08 TARGET 1.20.1.2"
BEGIN_V2 = "BATCH_BEGIN SOURCE F001_FIX_12 TARGET 1.20.1.2 SCOPE FULL"
BEGIN_V3 = re.compile(r"BATCH_BEGIN SOURCE F001_FIX_12 TARGET 1\.20\.1\.2 SCOPE SELECTED VIEW (REALMS|HOLDINGS|MY_REALM)")
VIEWS = ("REALMS", "HOLDINGS", "MY_REALM")
RGB = {"PRIMARY": [25, 105, 50], "SECONDARY": [145, 220, 150],
       "NEUTRAL": [65, 70, 80]}
DEFAULT_MAX_BYTES = 512 * 1024 * 1024
MAX_LINE_BYTES = 1024 * 1024
MARKER = re.compile(
    r"^\[[^\]\r\n]+\]\[D\]\[jomini_effect_impl\.cpp:\d+\]: "
    r"file: common/scripted_effects/dynmap_r016\.txt line: \d+ "
    r"\([a-z0-9_]+\): DYNMAP_R016 AUDIT V1 (.+)$")
MARKER_V2 = re.compile(MARKER.pattern.replace("AUDIT V1", "AUDIT V2"))
MARKER_V3 = re.compile(MARKER.pattern.replace("AUDIT V1", "AUDIT V3"))
MARKER_V4 = re.compile(MARKER.pattern.replace("AUDIT V1", "AUDIT V4"))
MARKER_DIAG = re.compile(MARKER.pattern.replace("AUDIT V1", "DIAG V2"))
MARKER_DIAG_V3 = re.compile(MARKER.pattern.replace("AUDIT V1", "DIAG V3"))
SCOPE = re.compile(r"^\[[^\]\r\n]+\]\[D\]\[effectimpl\.cpp:\d+\]: (.+)$")
IDENTITY = re.compile(
    r"^(.*?) \(Internal ID: (\d+)(?: - (Historical ID|Internal Key):? "
    r"([A-Za-z0-9_.:-]*))?\) (?:\x15weak )?"
    r"\((Character|Dynasty|Landed_title) - (\d+)\)(?:\x15!)?$")
IDENTITY_FIELDS = {"SUBJECT": "Character", "DYNASTY": "Dynasty",
                   "LIEGE": "Character", "TOP": "Character",
                   "COUNTY_BEGIN": "Landed_title", "EXPECT_COUNTY": "Landed_title"}


class Invalid(ValueError):
    pass


def identity(text, expected):
    """Native current scope only; labels never identify an object."""
    match = IDENTITY.fullmatch(text)
    if not match:
        raise Invalid("unrecognized native identity shape")
    label, runtime, kind, external, typ, repeated = match.groups()
    if typ != expected or runtime != repeated:
        raise Invalid("wrong native scope type or conflicting runtime IDs")
    if typ == "Character" and kind not in (None, "Historical ID"):
        raise Invalid("character historical/runtime namespaces confused")
    if typ == "Character" and kind == "Historical ID" and not external:
        raise Invalid("empty historical character identity")
    if typ == "Dynasty" and kind not in (None, "Internal Key"):
        raise Invalid("Dynasty runtime/database namespaces confused")
    if typ == "Landed_title" and (kind != "Internal Key" or not external):
        raise Invalid("missing stable database key")
    if typ == "Landed_title" and not external.startswith("c_"):
        raise Invalid("non-county title in county record")
    return {"type": typ, "runtime_id": runtime, "label": label,
            "historical_id": external if kind == "Historical ID" else None,
            "key": (external or None) if kind == "Internal Key" else None}


def ref(obj):
    return None if obj is None else (obj["type"], obj["runtime_id"])


def actor_signature(actor):
    return tuple(ref(actor[field]) for field in ("subject", "dynasty", "liege", "top")) + tuple(
        actor[field] for field in ("no_liege", "liege_self", "top_self", "independent"))


def location(token):
    return {"input": token["input"], "line": token["line"]}


class Cursor:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]["text"] if self.pos < len(self.tokens) else None

    def take(self, expected=None):
        if self.pos >= len(self.tokens):
            raise Invalid("missing " + str(expected))
        token = self.tokens[self.pos]
        self.pos += 1
        if expected is not None and token["text"] != expected:
            raise Invalid("line %s: expected %s, found %s" % (
                token["line"], expected, token["text"]))
        return token

    def obj(self, field):
        token = self.take(field)
        if token.get("identity_error") or "identity" not in token:
            raise Invalid("line %s: %s" % (
                token["line"], token.get("identity_error", "missing native identity")))
        return dict(token["identity"], source=location(token),
                    identity_line=token["identity_line"])

    def nullable(self, field):
        if self.peek() == field + "_NULL":
            self.take()
            return None
        return self.obj(field)

    def flag(self, field):
        token = self.take()
        if token["text"] not in (field + " YES", field + " NO"):
            raise Invalid("line %s: missing/invalid %s flag" % (token["line"], field))
        return token["text"].endswith(" YES")


def parse_actor(cur, role):
    start = cur.take("ACTOR_BEGIN " + role)
    actor = {"role": role, "source": location(start), "subject": cur.obj("SUBJECT"),
             "dynasty": cur.nullable("DYNASTY"), "liege": cur.nullable("LIEGE")}
    actor["no_liege"] = cur.flag("NO_LIEGE")
    actor["liege_self"] = cur.flag("LIEGE_SELF")
    actor["top"] = cur.nullable("TOP")
    actor["top_self"] = cur.flag("TOP_SELF")
    actor["independent"] = cur.flag("INDEPENDENT")
    cur.take("ACTOR_END")
    return actor


def parse_batch(tokens, sequence):
    if tokens[0].get("schema") == 2:
        return parse_batch_v2(tokens, sequence)
    if tokens[0].get("schema") == 3:
        return parse_batch_v3(tokens, sequence)
    cur = Cursor(tokens)
    first = cur.take(BEGIN)
    batch = {"sequence": sequence, "source": location(first),
             "end": location(tokens[-1]), "source_version": "F001_DUMP_08",
             "schema": 1, "operation_scope": "FULL", "target": "1.20.1.2", "records": [], "errors": []}
    if cur.peek() and cur.peek().startswith("REJECT "):
        batch.update(availability="UNAVAILABLE", rejection=cur.take()["text"])
        cur.take("BATCH_END")
        if cur.peek() is not None:
            raise Invalid("tokens after rejected batch")
        return batch
    batch["player"] = parse_actor(cur, "PLAYER")
    batch["availability"] = "AVAILABLE" if batch["player"]["dynasty"] else "UNAVAILABLE"
    cur.take("ROSTER_BEGIN")
    roster = []
    while cur.peek() == "EXPECT_COUNTY":
        token = cur.tokens[cur.pos]
        roster.append({"county": cur.obj("EXPECT_COUNTY"), "source": location(token)})
    cur.take("ROSTER_END")
    batch["roster"] = roster
    for view in VIEWS:
        cur.take("VIEW_BEGIN " + view)
        while cur.peek() == "COUNTY_BEGIN":
            start = cur.tokens[cur.pos]
            county = cur.obj("COUNTY_BEGIN")
            holder = None
            if cur.peek() == "HOLDER_NULL":
                cur.take()
            else:
                holder = parse_actor(cur, "HOLDER")
            cur.take("SENIORS_BEGIN")
            seniors = []
            while cur.peek() == "ACTOR_BEGIN SENIOR":
                seniors.append(parse_actor(cur, "SENIOR"))
            cur.take("SENIORS_END")
            result = cur.take()
            match = re.fullmatch(r"RESULT (PRIMARY|SECONDARY|NEUTRAL) RGB (\d{1,3}) (\d{1,3}) (\d{1,3}) WRITES_SUPPRESSED", result["text"])
            if not match:
                raise Invalid("line %s: missing/invalid actual result" % result["line"])
            if any(int(match[i]) > 255 for i in (2, 3, 4)):
                raise Invalid("line %s: intended RGB outside byte range" % result["line"])
            end = cur.take("COUNTY_END")
            batch["records"].append({"view": view, "county": county, "holder": holder,
                "seniors": seniors, "actual_role": match[1],
                "intended_rgb": [int(match[i]) for i in (2, 3, 4)],
                "write_status": "SUPPRESSED", "source": location(start),
                "result_source": location(result), "end": location(end)})
        cur.take("VIEW_END " + view)
    cur.take("BATCH_END")
    if cur.peek() is not None:
        raise Invalid("unexpected tokens after batch end")
    return batch


COUNTER_FIELDS = ("total", "primary", "secondary", "neutral", "held", "unheld",
                  "holder_no_dynasty", "holder_match", "senior_match", "top_match",
                  "subtree", "attempted_writes")
NATIVE_KEYS = {"dynmap_r016_out_" + field: field for field in COUNTER_FIELDS}
NATIVE_KEYS.update({"dynmap_r016_out_roster": "roster", "dynmap_r016_out_actors": "actors"})
SUMMARY_NATIVE_KEYS = {key for key in NATIVE_KEYS if key not in ("dynmap_r016_out_roster", "dynmap_r016_out_actors")}
NATIVE_COUNT = re.compile(r"([0-9]{1,15})(?:\.([0-9]+))?")


def parse_native_targets(lines, expected):
    """Parse one target-build debug_log_scopes block without deriving counts."""
    if any("DYNMAP_R016" in line for line in lines):
        raise Invalid("nested/interleaved operation marker inside native counter block")
    roots = sum(line.startswith("Root: ") for line in lines)
    sections = sum(line == "Saved event targets:" for line in lines)
    if roots != 1 or sections != 1:
        raise Invalid("native dump must contain exactly one Root and Saved event targets header")
    root_at = next(i for i, line in enumerate(lines) if line.startswith("Root: "))
    section_at = lines.index("Saved event targets:")
    if root_at >= section_at:
        raise Invalid("native dump Root must precede saved targets")
    if root_at != 1 or not SCOPE.fullmatch(lines[0]):
        raise Invalid("native dump must begin with immediate current identity followed by Root")
    current_match = SCOPE.fullmatch(lines[0])
    root_match = re.fullmatch(r"Root: (.+)", lines[root_at])
    current_identity = identity(current_match[1], "Character")
    root_identity = identity(root_match[1], "Character")
    if ref(current_identity) != ref(root_identity):
        raise Invalid("native current and Root identities disagree")
    values, seen = {}, set()
    for line in lines[section_at + 1:]:
        if not line:
            continue
        if ": " not in line:
            raise Invalid("malformed native saved-target line")
        key, raw = line.split(": ", 1)
        if key.startswith("dynmap_r016_out_"):
            if key not in NATIVE_KEYS or key in seen:
                raise Invalid("unknown or duplicate dynmap counter target")
            if key not in expected:
                raise Invalid("unexpected phase-specific dynmap counter target")
            match = NATIVE_COUNT.fullmatch(raw)
            if not match or (match[2] is not None and any(c != "0" for c in match[2])):
                raise Invalid("native counter is not an exact nonnegative integer")
            try:
                number = Decimal(raw)
            except InvalidOperation:
                raise Invalid("invalid native counter number")
            if number > 9999999999:
                raise Invalid("native counter exceeds supported integer range")
            values[NATIVE_KEYS[key]] = int(number)
            seen.add(key)
    if seen != set(expected):
        raise Invalid("native dump is missing required phase counters")
    return values, current_identity
RESULT = re.compile(r"RESULT (PRIMARY|SECONDARY|NEUTRAL) RGB (\d{1,3}) (\d{1,3}) (\d{1,3}) WRITES_SUPPRESSED")


def parse_counters(cur):
    token = cur.take()
    pattern = "COUNTS " + " ".join(field.upper() + r" (\d{1,10})" for field in COUNTER_FIELDS)
    match = re.fullmatch(pattern, token["text"])
    if not match:
        raise Invalid("missing/invalid V2 view counters")
    return dict(zip(COUNTER_FIELDS, map(int, match.groups())))


def graph_chain(subject, actors):
    """V2 definitions include all ordinary links, including the player's ancestry."""
    chain, seen = [], set()
    key = ref(subject)
    while True:
        if key in seen:
            raise Invalid("ordinary liege cycle in V2 actor definitions")
        if key not in actors:
            raise Invalid("unresolved V2 actor/ordinary parent reference")
        actor = actors[key]
        seen.add(key)
        chain.append(actor)
        parent = ref(actor["liege"])
        if parent is None or parent == key:
            break
        key = parent
    terminal = ref(chain[-1]["subject"])
    for actor in chain:
        if actor["top"] is None or ref(actor["top"]) != terminal:
            raise Invalid("null/conflicting V2 explicit top versus ordinary terminal")
    return chain


def parse_batch_v2(tokens, sequence, selected_view=None):
    cur = Cursor(tokens)
    if selected_view is None:
        first = cur.take(BEGIN_V2)  # SUMMARY/SAMPLES can never masquerade as FULL.
    else:
        framing = BEGIN_V3.fullmatch(cur.peek() or "")
        if framing is None or framing[1] != selected_view:
            raise Invalid("V3 framing and selected view disagree")
        first = cur.take(framing[0])
    batch = {"sequence": sequence, "source": location(first), "end": location(tokens[-1]),
             "source_version": "F001_FIX_12", "schema": 2 if selected_view is None else 3,
             "operation_scope": "FULL" if selected_view is None else "SELECTED", "selected_view": selected_view,
             "target": "1.20.1.2", "records": [], "errors": []}
    if cur.peek() and cur.peek().startswith("REJECT "):
        batch.update(availability="UNAVAILABLE", rejection=cur.take()["text"])
        cur.take("BATCH_END")
        if cur.peek() is not None:
            raise Invalid("tokens after rejected batch")
        return batch
    player = parse_actor(cur, "PLAYER")
    batch["player"] = player
    batch["availability"] = "AVAILABLE" if player["dynasty"] else "UNAVAILABLE"
    actors = {ref(player["subject"]): player}

    def definition():
        actor = parse_actor(cur, "DEF")
        key = ref(actor["subject"])
        if key in actors:
            raise Invalid("duplicate/conflicting V2 actor definition")
        actors[key] = actor

    while cur.peek() == "ACTOR_BEGIN DEF":
        definition()
    cur.take("ROSTER_BEGIN")
    roster = []
    while cur.peek() in ("ACTOR_BEGIN DEF", "COUNTY_BEGIN"):
        if cur.peek() == "ACTOR_BEGIN DEF":
            definition()
            continue
        start = cur.tokens[cur.pos]
        county = cur.obj("COUNTY_BEGIN")
        holder_ref = cur.nullable("HOLDER")
        cur.take("COUNTY_END")
        roster.append({"county": county, "holder_ref": holder_ref, "source": location(start)})
    count_token = cur.take()
    match = re.fullmatch(r"ROSTER_COUNTS COUNT (\d{1,10}) ACTORS (\d{1,10})", count_token["text"])
    if not match:
        raise Invalid("missing/invalid V2 roster/actor counts")
    if int(match[1]) != len(roster) or int(match[2]) != len(actors):
        batch["errors"].append("V2 declared roster/actor counts disagree")
    batch["declared_roster_count"], batch["declared_actor_count"] = map(int, match.groups())
    cur.take("ROSTER_END")
    batch["roster"] = roster
    batch["actor_definitions"] = list(actors.values())
    # Validate every definition, including actors outside any holder's chain.
    chains = {key: graph_chain(a["subject"], actors) for key, a in actors.items()}
    county_map = {}
    for item in roster:
        key = ref(item["county"])
        if key in county_map:
            batch["errors"].append("duplicate county in V2 roster")
        county_map[key] = item
        if item["holder_ref"] is not None and ref(item["holder_ref"]) not in actors:
            raise Invalid("unresolved V2 holder actor reference")
    batch["view_counters"] = {}
    for view in ((selected_view,) if selected_view is not None else VIEWS):
        cur.take("VIEW_BEGIN " + view)
        rows = []
        while cur.peek() and cur.peek().startswith("RESULT "):
            token = cur.tokens[cur.pos]
            match = RESULT.fullmatch(token["text"])
            if not match or any(int(match[i]) > 255 for i in (2, 3, 4)):
                raise Invalid("missing/invalid V2 actual result/intended RGB")
            county = cur.obj(token["text"])
            item = county_map.get(ref(county))
            if item is None:
                raise Invalid("V2 result references unknown roster county")
            chain = chains[ref(item["holder_ref"])] if item["holder_ref"] else []
            row = {"view": view, "county": county, "holder": chain[0] if chain else None,
                   "seniors": chain[1:], "actual_role": match[1],
                   "intended_rgb": [int(match[i]) for i in (2, 3, 4)],
                   "write_status": "SUPPRESSED", "source": location(token),
                   "result_source": location(token), "end": location(token)}
            rows.append(row)
        declared = parse_counters(cur)
        batch["view_counters"][view] = declared
        # Reconcile emission counts and match/subtree indicators independently of role.
        expected = dict.fromkeys(COUNTER_FIELDS, 0)
        dynasty = ref(player["dynasty"])
        for row in rows:
            expected["total"] += 1
            expected[row["actual_role"].lower()] += 1
            holder = row["holder"]
            if holder is None:
                expected["unheld"] += 1
                continue
            expected["held"] += 1
            chain = [holder] + row["seniors"]
            expected["holder_no_dynasty"] += holder["dynasty"] is None
            expected["holder_match"] += ref(holder["dynasty"]) == dynasty and dynasty is not None
            expected["senior_match"] += any(ref(a["dynasty"]) == dynasty for a in chain[1:]) and dynasty is not None
            expected["top_match"] += ref(chain[-1]["dynasty"]) == dynasty and dynasty is not None
            expected["subtree"] += any(ref(a["subject"]) == ref(player["subject"]) for a in chain)
        if declared != expected or declared["total"] != len(roster):
            batch["errors"].append(view + ": V2 counters/roster/actual records disagree")
        batch["records"].extend(rows)
        cur.take("VIEW_END " + view)
    cur.take("BATCH_END")
    if cur.peek() is not None:
        raise Invalid("unexpected tokens after V2 batch end")
    return batch


def parse_batch_v3(tokens, sequence):
    match = BEGIN_V3.fullmatch(tokens[0]["text"])
    if not match:
        raise Invalid("V3 batch must explicitly declare exactly one selected view")
    view = match[1]
    batch = parse_batch_v2(tokens, sequence, selected_view=view)
    # Keep the framing version explicit; V2 remains a distinct historical all-view contract.
    batch["schema"] = 3
    return batch


def chain_for(record):
    """Reconstruct unordered child -> ordinary parent edges, reconcile ALL tops.

    Neither no-liege nor the independence predicate is the semantic oracle.
    Self-parent is a terminal link only when explicit top identity agrees.
    A null top leaves T unverified, even if a no-liege predicate says YES.
    """
    holder, seniors = record["holder"], record["seniors"]
    if holder is None:
        if seniors:
            raise Invalid("unheld county has seniors")
        return [], None
    nodes = {ref(holder["subject"]): holder}
    for senior in seniors:
        key = ref(senior["subject"])
        if key in nodes:
            raise Invalid("duplicate senior or holder included among seniors")
        nodes[key] = senior
    chain, seen = [], set()
    key = ref(holder["subject"])
    while True:
        if key in seen:
            raise Invalid("ordinary liege cycle")
        if key not in nodes:
            raise Invalid("ordinary liege edge has no senior record")
        seen.add(key)
        actor = nodes[key]
        chain.append(actor)
        parent = ref(actor["liege"])
        if parent is None or parent == key:
            break
        key = parent
    if seen != set(nodes):
        raise Invalid("senior iterator and ordinary parent chain disagree (gap or extra senior)")
    terminal = ref(chain[-1]["subject"])
    for actor in chain:
        if actor["top"] is None:
            raise Invalid("null top_liege: highest ordinary ruler unverified")
        if ref(actor["top"]) != terminal:
            raise Invalid("top_liege contradicts reconstructed ordinary terminal")
    return chain, chain[-1]


def expected_role(view, player, chain, top):
    if player["dynasty"] is None:
        return "UNAVAILABLE", "player has no Dynasty"
    if not chain:
        return "NEUTRAL", "county is unheld"
    dynasty = ref(player["dynasty"])
    dynastic = [ref(actor["dynasty"]) == dynasty for actor in chain]
    subtree = any(ref(actor["subject"]) == ref(player["subject"]) for actor in chain)
    if view == "REALMS":
        primary, secondary = ref(top["dynasty"]) == dynasty, any(dynastic)
        reason = "highest ordinary ruler belongs to player Dynasty"
    elif view == "HOLDINGS":
        primary, secondary = dynastic[0], any(dynastic[1:])
        reason = "holder belongs to player Dynasty"
    else:
        primary, secondary = subtree, any(dynastic)
        reason = "holder is player or ordinary descendant of player"
    if primary:
        return "PRIMARY", reason + "; Primary precedence"
    if secondary:
        return "SECONDARY", "dynastic holder/senior outside Primary condition"
    return "NEUTRAL", "no player-subtree/Dynasty match for this view"


def verify_batch(batch):
    if batch["availability"] == "UNAVAILABLE" and "player" not in batch:
        batch.update(record_completeness="UNVERIFIED", classification_match="UNVERIFIED",
                     intended_rgb_mapping="UNVERIFIED")
        return
    errors = batch["errors"]
    player = batch["player"]
    roster = batch["roster"]
    keys = [item["county"]["key"] for item in roster]
    if not keys:
        errors.append("empty county roster/zero records cannot establish a pass")
    if len(keys) != len(set(keys)):
        errors.append("duplicate county in roster")
    expected_views = (batch["selected_view"],) if batch.get("operation_scope") == "SELECTED" else VIEWS
    for view in expected_views:
        actual = [r["county"]["key"] for r in batch["records"] if r["view"] == view]
        if len(actual) != len(set(actual)):
            errors.append(view + ": duplicate county record")
        if set(actual) != set(keys):
            errors.append(view + ": missing or extra county versus batch roster")
    # Check stable metadata for every object reference; runtime IDs are batch-local.
    identities, stable_ids, actors = {}, {}, {}

    def check_identity(obj):
        if obj is None:
            return
        key = ref(obj)
        meta = (obj["historical_id"], obj["key"])
        if key in identities and identities[key] != meta:
            errors.append("inconsistent identity metadata for %s:%s" % key)
        identities[key] = meta
        if obj["key"] is not None:
            stable = (obj["type"], obj["key"])
            if stable in stable_ids and stable_ids[stable] != key:
                errors.append("stable database key maps to conflicting runtime identities")
            stable_ids[stable] = key

    def check_actor(actor):
        for field in ("subject", "dynasty", "liege", "top"):
            check_identity(actor[field])
        key = ref(actor["subject"])
        signature = actor_signature(actor)
        if key in actors and actors[key] != signature:
            errors.append("character data changes within batch: %s:%s" % key)
        actors[key] = signature
        if actor["no_liege"] != (actor["liege"] is None):
            errors.append("NO_LIEGE contradicts explicit link")
        if actor["liege_self"] != (ref(actor["liege"]) == key):
            errors.append("LIEGE_SELF contradicts explicit identity")
        if actor["top_self"] != (ref(actor["top"]) == key):
            errors.append("TOP_SELF contradicts explicit identity")

    check_actor(player)
    for actor in batch.get("actor_definitions", []):
        check_actor(actor)
    for item in roster:
        check_identity(item["county"])
        check_identity(item.get("holder_ref"))
    county_holders = {}
    for record in batch["records"]:
        check_identity(record["county"])
        key = record["county"]["key"]
        holder_key = ref(record["holder"]["subject"]) if record["holder"] else None
        if key in county_holders and county_holders[key] != holder_key:
            errors.append("county holder changes between views: " + key)
        county_holders[key] = holder_key
        for actor in ([record["holder"]] if record["holder"] else []) + record["seniors"]:
            check_actor(actor)
    batch["errors"] = list(dict.fromkeys(errors))
    for record in batch["records"]:
        record["intended_rgb_match"] = record["intended_rgb"] == RGB[record["actual_role"]]
        record["runtime_storage"] = "UNVERIFIED: writes suppressed; no stored/pixel RGB observed"
        record["expected_role"] = None
        record["ordinary_chain"] = []
        try:
            if batch["errors"]:
                raise Invalid("batch identity/roster errors invalidate record context")
            if batch["availability"] != "AVAILABLE":
                raise Invalid("invalid player/Dynasty: classification unavailable")
            chain, top = chain_for(record)
            record["ordinary_chain"] = [a["subject"] for a in chain]
            record["highest_ordinary_ruler"] = top["subject"] if top else None
            expected, reason = expected_role(record["view"], player, chain, top)
            record.update(expected_role=expected, expected_reason=reason,
                          record_completeness="COMPLETE",
                          classification_match="MATCH" if expected == record["actual_role"] else "MISMATCH")
        except Invalid as exc:
            record.update(expected_reason=str(exc), record_completeness="INCOMPLETE",
                          classification_match="UNVERIFIED")
    complete = bool(batch["records"]) and not batch["errors"] and all(
        r["record_completeness"] == "COMPLETE" for r in batch["records"])
    batch["record_completeness"] = "COMPLETE" if complete else "INCOMPLETE"
    batch["classification_match"] = ("MISMATCH" if any(
        r["classification_match"] == "MISMATCH" for r in batch["records"]) else
        "MATCH" if complete else "UNVERIFIED")
    batch["intended_rgb_mapping"] = ("MISMATCH" if any(
        not r["intended_rgb_match"] for r in batch["records"]) else
        "MATCH" if complete else "UNVERIFIED")


def analyze_paths(paths, max_bytes=DEFAULT_MAX_BYTES):
    """Stream finite explicit captures. A batch may not span input files."""
    batches, errors, inputs, diagnostics = [], [], [], []
    total_bytes, sequence = 0, 0
    for input_index, path in enumerate(paths, 1):
        path = Path(path)
        tokens, pending, current, diagnostic, native_dump = [], None, None, None, None
        digest, size, line_no = hashlib.sha256(), 0, 0
        try:
            with path.open("rb") as handle:
                while True:
                    raw = handle.readline(MAX_LINE_BYTES + 1)
                    if not raw:
                        break
                    size += len(raw)
                    total_bytes += len(raw)
                    line_no += 1
                    digest.update(raw)
                    if len(raw) > MAX_LINE_BYTES or total_bytes > max_bytes:
                        raise Invalid("finite byte/line limit exceeded; capture NOT complete")
                    text = raw.rstrip(b"\r\n").decode("utf-8", errors="backslashreplace")
                    if not raw.endswith(b"\n") and (current is not None or diagnostic is not None or "DYNMAP_R016 AUDIT" in text or "DYNMAP_R016 DIAG" in text):
                        errors.append({"input": input_index, "line": line_no,
                                       "error": "unterminated audit capture line"})
                    if pending is not None:
                        match = SCOPE.fullmatch(text)
                        try:
                            if not match:
                                raise Invalid("identity must be the immediate native current-scope line")
                            pending["identity"] = identity(match[1], pending["identity_expected"])
                            pending["identity_line"] = line_no
                        except Invalid as exc:
                            pending["identity_error"] = str(exc)
                        pending = None
                        if match:
                            continue
                    diag_v3 = MARKER_DIAG_V3.fullmatch(text)
                    if native_dump is not None:
                        end_marker = MARKER_DIAG_V3.fullmatch(text)
                        end = re.fullmatch(r"COUNTERS_END PHASE (SUMMARY|SAMPLES) VIEW (REALMS|HOLDINGS|MY_REALM)", end_marker[1]) if end_marker else None
                        if end:
                            try:
                                if (end[1], end[2]) != (native_dump["phase"], native_dump["view"]):
                                    raise Invalid("native counter end marker phase/view mismatch")
                                vals, context = parse_native_targets(native_dump["lines"], SUMMARY_NATIVE_KEYS)
                                if diagnostic is None or (diagnostic["operation_scope"], diagnostic["view"]) != (end[1], end[2]):
                                    raise Invalid("native counter block outside matching diagnostic operation")
                                if diagnostic.get("native_counters") is not None:
                                    raise Invalid("duplicate native counter block")
                                diagnostic["native_counters"] = vals
                                diagnostic["native_context"] = {"type": context["type"], "runtime_id": context["runtime_id"]}
                                diagnostic["native_counter_block"] = {"phase": native_dump["phase"], "view": native_dump["view"],
                                    "input": input_index, "begin_line": native_dump["begin_line"], "end_line": line_no}
                                diagnostic["counter_source"] = "CK3 debug_log_scopes / Saved event targets"
                                if (vals["total"] != vals["primary"] + vals["secondary"] + vals["neutral"] or
                                        vals["total"] != vals["held"] + vals["unheld"] or
                                        any(vals[f] > vals["held"] for f in ("holder_no_dynasty", "holder_match", "senior_match", "top_match", "subtree"))):
                                    raise Invalid("native diagnostic counters disagree arithmetically")
                                if end[1] == "SUMMARY":
                                    diagnostic["summary"] = vals
                            except Invalid as exc:
                                errors.append({"input": input_index, "line": line_no, "error": str(exc)})
                            native_dump = None
                            continue
                        end_marker = MARKER_V4.fullmatch(text)
                        audit_end = re.fullmatch(r"COUNTERS_END PHASE (ROSTER|VIEW) VIEW (SELECTED|REALMS|HOLDINGS|MY_REALM)", end_marker[1]) if end_marker else None
                        if audit_end:
                            try:
                                phase, view = audit_end[1], audit_end[2]
                                if (phase, view) != (native_dump["phase"], native_dump["view"]):
                                    raise Invalid("native audit counter end marker phase/view mismatch")
                                expected = {"dynmap_r016_out_roster", "dynmap_r016_out_actors"} if phase == "ROSTER" else SUMMARY_NATIVE_KEYS
                                vals, context = parse_native_targets(native_dump["lines"], expected)
                                if current is None:
                                    raise Invalid("native audit counters outside a batch")
                                if phase == "ROSTER":
                                    tokens.append({"text": "ROSTER_COUNTS COUNT %d ACTORS %d" % (vals["roster"], vals["actors"]), "input": input_index, "line": line_no, "schema": 4, "native_context": (context["type"], context["runtime_id"]), "native_block": {"phase": phase, "view": view, "input": input_index, "begin_line": native_dump["begin_line"], "end_line": line_no}})
                                else:
                                    tokens.append({"text": "COUNTS " + " ".join(field.upper() + " " + str(vals[field]) for field in COUNTER_FIELDS), "input": input_index, "line": line_no, "schema": 4, "native_context": (context["type"], context["runtime_id"]), "native_block": {"phase": phase, "view": view, "input": input_index, "begin_line": native_dump["begin_line"], "end_line": line_no}})
                            except Invalid as exc:
                                errors.append({"input": input_index, "line": line_no, "error": str(exc)})
                            native_dump = None
                            continue
                        else:
                            native_dump["lines"].append(text)
                        continue
                    if diag_v3:
                        payload = diag_v3[1]
                        token = {"text": payload, "input": input_index, "line": line_no}
                        try:
                            begin = re.fullmatch(r"BEGIN SOURCE F004_NATIVE_14 TARGET 1\.20\.1\.2 BUILD 26046173 SCOPE (SUMMARY|SAMPLES) VIEW (REALMS|HOLDINGS|MY_REALM)", payload)
                            counters = re.fullmatch(r"COUNTERS_BEGIN PHASE (SUMMARY|SAMPLES) VIEW (REALMS|HOLDINGS|MY_REALM)", payload)
                            if current is not None:
                                raise Invalid("diagnostic operation interleaved inside full batch")
                            if begin:
                                if diagnostic is not None:
                                    raise Invalid("nested diagnostic operation")
                                diagnostic = {"schema": 3, "source_version": "F004_NATIVE_14", "target": "1.20.1.2", "build": "26046173",
                                    "operation_scope": begin[1], "view": begin[2], "write_policy": "PAINT_ATTEMPTS; no stored/pixel receipt",
                                    "source": location(token), "samples": dict.fromkeys(RGB, 0), "details": 0,
                                    "summary": None, "native_counters": None, "availability": "AVAILABLE",
                                    "validation": "FRAMING_AND_BOUNDS_ONLY; not a full-map classification audit"}
                            elif counters:
                                if diagnostic is None or native_dump is not None or (diagnostic["operation_scope"], diagnostic["view"]) != (counters[1], counters[2]):
                                    raise Invalid("unexpected or nested native counter block")
                                native_dump = {"phase": counters[1], "view": counters[2], "lines": [], "begin_line": line_no}
                            elif diagnostic is None:
                                raise Invalid("diagnostic marker outside framed operation")
                            elif payload.startswith(("SAMPLE ROLE ", "DETAIL ROLE ")):
                                sm = re.fullmatch(r"(SAMPLE|DETAIL) ROLE (primary|secondary|neutral)", payload)
                                if not sm or diagnostic["operation_scope"] != "SAMPLES":
                                    raise Invalid("invalid/unexpected bounded diagnostic sample")
                                if sm[1] == "SAMPLE": diagnostic["samples"][sm[2].upper()] += 1
                                else: diagnostic["details"] += 1
                                if max(diagnostic["samples"].values()) > 10 or diagnostic["details"] > 20:
                                    raise Invalid("diagnostic sample/detail bounds exceeded")
                            elif payload == "UNAVAILABLE": diagnostic["availability"] = "UNAVAILABLE"
                            elif payload == "END":
                                if diagnostic["availability"] == "AVAILABLE" and diagnostic.get("native_counters") is None:
                                    raise Invalid("available DIAG V3 operation needs exactly one complete native counter block")
                                if diagnostic["operation_scope"] == "SUMMARY" and diagnostic.get("summary") is None:
                                    raise Invalid("summary DIAG V3 operation lacks native declaration")
                                if diagnostic["availability"] == "UNAVAILABLE" and diagnostic.get("native_counters") is not None:
                                    raise Invalid("unavailable operation cannot contain native counters")
                                diagnostic.update(end=location(token), framing="COMPLETE")
                                diagnostics.append(diagnostic); diagnostic = None
                            elif payload not in ("COUNTY", "HOLDER", "HOLDER_NO_DYNASTY", "TOP_UNAVAILABLE", "UNHELD", "ZERO_BARONY_WRITES"):
                                raise Invalid("unsupported DIAG V3 marker")
                        except Invalid as exc:
                            errors.append(dict(location(token), error=str(exc)))
                        continue
                    if re.match(r"^dynmap_r016_out_[A-Za-z0-9_]+:\s*", text):
                        if diagnostic is not None or (current is not None and tokens and tokens[0].get("schema") == 4):
                            errors.append({"input": input_index, "line": line_no,
                                           "error": "native counter target outside its framed counter block"})
                        continue
                    diag_marker = MARKER_DIAG.fullmatch(text)
                    if diag_marker:
                        payload = diag_marker[1]
                        token = {"text": payload, "input": input_index, "line": line_no}
                        try:
                            if current is not None:
                                raise Invalid("diagnostic operation interleaved inside full batch")
                            if payload.startswith("BEGIN "):
                                match = re.fullmatch(r"BEGIN SOURCE F001_FIX_12 SCOPE (SUMMARY|SAMPLES) VIEW (REALMS|HOLDINGS|MY_REALM)", payload)
                                if not match or diagnostic is not None:
                                    raise Invalid("unsupported/nested diagnostic operation")
                                diagnostic = {"schema": 2, "source_version": "F001_FIX_12",
                                              "operation_scope": match[1], "view": match[2],
                                              "write_policy": "PAINT_ATTEMPTS; no stored/pixel receipt",
                                              "source": location(token), "samples": dict.fromkeys(RGB, 0),
                                              "details": 0, "summary": None, "availability": "AVAILABLE",
                                              "validation": "FRAMING_AND_BOUNDS_ONLY; not a full-map classification audit"}
                            elif diagnostic is None:
                                raise Invalid("diagnostic marker outside framed operation")
                            elif payload.startswith("SAMPLE ROLE ") or payload.startswith("DETAIL ROLE "):
                                match = re.fullmatch(r"(SAMPLE|DETAIL) ROLE (primary|secondary|neutral)", payload)
                                if not match or diagnostic["operation_scope"] != "SAMPLES":
                                    raise Invalid("invalid/unexpected bounded diagnostic sample")
                                if match[1] == "SAMPLE":
                                    diagnostic["samples"][match[2].upper()] += 1
                                else:
                                    diagnostic["details"] += 1
                                if max(diagnostic["samples"].values()) > 10 or diagnostic["details"] > 20:
                                    raise Invalid("diagnostic sample/detail bounds exceeded")
                            elif payload.startswith("SUMMARY "):
                                if diagnostic["summary"] is not None:
                                    raise Invalid("duplicate diagnostic summary")
                                counter_token = dict(token, text="COUNTS " + payload[len("SUMMARY "):])
                                counts = parse_counters(Cursor([counter_token]))
                                if (counts["total"] != counts["primary"] + counts["secondary"] + counts["neutral"] or
                                        counts["total"] != counts["held"] + counts["unheld"] or
                                        any(counts[f] > counts["held"] for f in ("holder_no_dynasty", "holder_match", "senior_match", "top_match", "subtree"))):
                                    raise Invalid("diagnostic summary counters disagree")
                                diagnostic["summary"] = counts
                            elif payload == "UNAVAILABLE":
                                diagnostic["availability"] = "UNAVAILABLE"
                            elif payload == "END":
                                if (diagnostic["summary"] is None) == (diagnostic["availability"] == "AVAILABLE"):
                                    raise Invalid("diagnostic operation needs exactly one summary or unavailable receipt")
                                diagnostic.update(end=location(token), framing="COMPLETE")
                                diagnostics.append(diagnostic)
                                diagnostic = None
                            elif payload not in ("COUNTY", "HOLDER", "HOLDER_NO_DYNASTY", "TOP_UNAVAILABLE", "UNHELD", "ZERO_BARONY_WRITES"):
                                raise Invalid("unsupported diagnostic marker")
                        except Invalid as exc:
                            errors.append(dict(location(token), error=str(exc)))
                        continue
                    marker = MARKER.fullmatch(text)
                    schema = 1
                    if not marker:
                        marker = MARKER_V2.fullmatch(text)
                        schema = 2
                    if not marker:
                        marker = MARKER_V3.fullmatch(text)
                        schema = 3
                    if not marker:
                        marker = MARKER_V4.fullmatch(text)
                        schema = 4
                    if not marker:
                        if (current is not None and SCOPE.fullmatch(text) and tokens and
                                tokens[-1].get("identity_expected") and
                                "identity" in tokens[-1]):
                            errors.append({"input": input_index, "line": line_no,
                                           "error": "ambiguous extra current-scope identity"})
                        if "DYNMAP_R016 AUDIT" in text or "DYNMAP_R016 DIAG" in text:
                            errors.append({"input": input_index, "line": line_no,
                                           "error": "unsupported/ambiguous audit marker shape or version"})
                        continue
                    payload = marker[1]
                    if schema == 4:
                        if payload.startswith("BATCH_BEGIN") and not re.fullmatch(r"BATCH_BEGIN SOURCE F004_NATIVE_14 TARGET 1\.20\.1\.2 BUILD 26046173 SCOPE SELECTED VIEW (REALMS|HOLDINGS|MY_REALM)", payload):
                            errors.append({"input": input_index, "line": line_no, "error": "unsupported native audit source, target or build"})
                            continue
                        payload = payload.replace("AUDIT V4", "AUDIT V3")
                        payload = payload.replace("BATCH_BEGIN SOURCE F004_NATIVE_14 TARGET 1.20.1.2 BUILD 26046173", "BATCH_BEGIN SOURCE F001_FIX_12 TARGET 1.20.1.2")
                    token = {"text": payload, "input": input_index, "line": line_no, "schema": schema}
                    v4_counters = re.fullmatch(r"COUNTERS_BEGIN PHASE (ROSTER|VIEW) VIEW (SELECTED|REALMS|HOLDINGS|MY_REALM)", marker[1]) if schema == 4 else None
                    if v4_counters:
                        if native_dump is not None:
                            errors.append(dict(location(token), error="nested native counter block"))
                        elif v4_counters[1] == "ROSTER" and v4_counters[2] != "SELECTED":
                            errors.append(dict(location(token), error="roster phase must declare SELECTED"))
                        elif v4_counters[1] == "VIEW" and v4_counters[2] not in VIEWS:
                            errors.append(dict(location(token), error="invalid selected-view counter phase"))
                        else:
                            pending = None
                            native_dump = {"phase": v4_counters[1], "view": v4_counters[2], "lines": [], "begin_line": line_no}
                        continue
                    expected_identity = IDENTITY_FIELDS.get(payload)
                    if schema in (2, 3, 4) and (payload == "HOLDER" or payload.startswith("RESULT ")):
                        expected_identity = "Character" if payload == "HOLDER" else "Landed_title"
                    if expected_identity:
                        token["identity_expected"] = expected_identity
                    if payload.startswith("BATCH_BEGIN"):
                        if diagnostic is not None:
                            errors.append(dict(location(token), error="full batch interleaved inside diagnostic operation"))
                        sequence += 1
                        if current is not None:
                            errors.append({"input": input_index, "line": line_no,
                                           "error": "nested batch; preceding batch truncated"})
                        current = sequence
                        tokens = [token]
                    elif current is None:
                        errors.append({"input": input_index, "line": line_no,
                                       "error": "audit record outside fully framed batch"})
                    else:
                        tokens.append(token)
                    if current is not None and expected_identity:
                        pending = token
                    if payload == "BATCH_END" and current is not None:
                        try:
                            if any(t["schema"] != tokens[0]["schema"] for t in tokens):
                                raise Invalid("mixed audit schema inside batch")
                            parse_tokens = tokens
                            native_schema = tokens[0]["schema"]
                            if native_schema == 4:
                                parse_tokens = [dict(t, schema=3) for t in tokens]
                            batch = parse_batch(parse_tokens, current)
                            if native_schema == 4:
                                batch["schema"] = 4
                                batch["source_version"] = "F004_NATIVE_14"
                                batch["target"] = "1.20.1.2"
                                batch["build"] = "26046173"
                                batch["counter_source"] = "CK3 debug_log_scopes / Saved event targets"
                                batch["native_counter_blocks"] = [t["native_block"] for t in tokens if t.get("native_block")]
                                expected_blocks = [("ROSTER", "SELECTED"), ("VIEW", batch["selected_view"])] if batch.get("availability") == "AVAILABLE" else []
                                if [(b["phase"], b["view"]) for b in batch["native_counter_blocks"]] != expected_blocks:
                                    raise Invalid("native counter block phases/views disagree with selected audit")
                                contexts = [t["native_context"] for t in tokens if t.get("native_context")]
                                expected_context = ref(batch["player"]["subject"]) if batch.get("player") else None
                                if batch.get("availability") == "AVAILABLE" and (len(contexts) != 2 or any(c != expected_context for c in contexts)):
                                    raise Invalid("native counter context does not match exactly the expected audit player/root")
                            verify_batch(batch)
                            batches.append(batch)
                        except Invalid as exc:
                            errors.append({"input": input_index, "line": line_no,
                                           "begin_line": tokens[0]["line"], "error": str(exc)})
                        current, tokens, pending = None, [], None
            if diagnostic is not None:
                errors.append({"input": input_index, "line": line_no, "error": "truncated diagnostic operation at end of input"})
            if native_dump is not None:
                errors.append({"input": input_index, "line": line_no, "error": "truncated native counter block"})
            if current is not None:
                errors.append({"input": input_index, "line": line_no,
                               "begin_line": tokens[0]["line"], "error": "truncated batch at end of input"})
            inputs.append({"input": input_index, "path": str(path), "bytes": size,
                           "sha256": digest.hexdigest(), "hash_scope": "complete input"})
        except (OSError, Invalid) as exc:
            errors.append({"input": input_index, "line": line_no, "error": str(exc)})
            inputs.append({"input": input_index, "path": str(path), "bytes_read": size,
                           "sha256": digest.hexdigest(), "hash_scope": "partial input only"})
            # No complete verdict when later input bytes were not inspected.
            break
    if not batches:
        errors.append({"error": "zero fully parsed batches; no semantic pass"})
    incomplete = bool(errors) or any(b["record_completeness"] != "COMPLETE" for b in batches)
    mismatch = any(b["classification_match"] == "MISMATCH" or
                   b["intended_rgb_mapping"] == "MISMATCH" for b in batches)
    status = "INCOMPLETE" if incomplete else "FAIL" if mismatch else "PASS"
    return {"schema": 4, "supported_capture_schemas": [1, 2, 3, 4], "status": status, "exit_code": 2 if incomplete else 1 if mismatch else 0,
            "capture_completeness": "INCOMPLETE" if errors else "COMPLETE",
            "inputs": inputs, "errors": errors, "batches": batches, "diagnostic_operations": diagnostics,
            "runtime_storage": "UNVERIFIED: no stored/pixel RGB evidence; full audits suppress writes",
            "coverage_limit": "Completeness is relative to emitted every_county roster; no independent engine census.",
            "selected_view_limit": "A V4 PASS covers only its explicitly named view; all three views require three separate selected-view batches. Historical V3 framing remains separately interpreted."}


def summary(report):
    lines = ["Classification audit: " + report["status"],
             "Capture framing: " + report["capture_completeness"], report["runtime_storage"],
             report["coverage_limit"]]
    if any(batch.get("schema") in (3, 4) for batch in report["batches"]):
        lines.append(report["selected_view_limit"])
    for error in report["errors"]:
        lines.append("Capture issue: " + json.dumps(error, ensure_ascii=True))
    for operation in report.get("diagnostic_operations", []):
        lines.append("Diagnostic %s %s: %s; %s" % (operation["operation_scope"], operation["view"], operation["framing"], operation["validation"]))
        if operation.get("counter_source"):
            lines.append("  Counter source: %s; build=%s/%s; expected native keys=%d; values=%s" % (
                operation["counter_source"], operation.get("target", "UNKNOWN"),
                operation.get("build", "UNKNOWN"), len(operation.get("native_counters", {})),
                json.dumps(operation.get("native_counters", {}), sort_keys=True)))
    for batch in report["batches"]:
        scope = ("scope=SELECTED view=" + batch["selected_view"]
                 if batch.get("operation_scope") == "SELECTED" else "scope=FULL")
        lines.append("Batch %s: %s records=%s completeness=%s roles=%s intended_RGB=%s availability=%s" % (
            batch["sequence"], scope, len(batch["records"]), batch["record_completeness"],
            batch["classification_match"], batch["intended_rgb_mapping"], batch["availability"]))
        if batch.get("counter_source"):
            lines.append("  Counter source: %s; build=%s/%s" % (batch["counter_source"],
                batch.get("target", "UNKNOWN"), batch.get("build", "UNKNOWN")))
        for error in batch["errors"]:
            lines.append("  Batch issue: " + error)
        if batch.get("rejection"):
            lines.append("  " + batch["rejection"])
        for record in batch["records"]:
            if record["classification_match"] != "MATCH" or not record["intended_rgb_match"]:
                lines.append("  %s %s actual=%s expected=%s RGB=%s at input %s line %s: %s" % (
                    record["view"], record["county"]["key"], record["actual_role"],
                    record["expected_role"], record["intended_rgb"], record["source"]["input"],
                    record["source"]["line"], record["expected_reason"]))
    return "\n".join(lines) + "\n"


def prepare_output(value):
    """Only a NEW, ignored repository-local directory; no raw data in Git."""
    repo = Path(__file__).resolve().parents[1]
    candidate = Path(value).absolute()
    for part in [candidate] + list(candidate.parents):
        if part.is_symlink():
            raise Invalid("output symlinks are refused")
    candidate = candidate.resolve()
    try:
        relative = candidate.relative_to(repo)
    except ValueError:
        raise Invalid("output must be an ignored directory inside this repository")
    if relative == Path(".") or candidate.exists():
        raise Invalid("output directory must be new")
    result = subprocess.run(["git", "check-ignore", "--quiet", "--", str(relative / "report.json")],
                            cwd=str(repo), check=False, capture_output=True)
    if result.returncode != 0:
        raise Invalid("output directory is not verified Git-ignored")
    candidate.mkdir(parents=True, exist_ok=False)
    return candidate


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("logs", nargs="+", help="explicit frozen debug-log capture path(s), in order")
    parser.add_argument("--output-dir", required=True, help="new Git-ignored repository-local directory")
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES,
                        help="finite aggregate input bound (default 512 MiB; exceeding means INCOMPLETE)")
    args = parser.parse_args(argv)
    try:
        if not 0 < args.max_bytes <= 2 * 1024 * 1024 * 1024:
            raise Invalid("max-bytes must be between 1 and 2 GiB")
        output = prepare_output(args.output_dir)
        report = analyze_paths(args.logs, args.max_bytes)
        (output / "report.json").write_text(json.dumps(report, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
        with (output / "counties.jsonl").open("w", encoding="utf-8") as handle:
            for batch in report["batches"]:
                for record in batch["records"]:
                    handle.write(json.dumps(dict(record, batch_sequence=batch["sequence"],
                        player=batch.get("player"), batch_source=batch["source"],
                        batch_completeness=batch["record_completeness"]), ensure_ascii=True) + "\n")
        rendered = summary(report)
        (output / "summary.txt").write_text(rendered, encoding="utf-8")
        print(rendered, end="")
        return report["exit_code"]
    except (Invalid, OSError) as exc:
        print("Classification audit: INCOMPLETE: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
