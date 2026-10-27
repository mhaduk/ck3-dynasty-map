"""Cooperative, file-backed implementation review lifecycle.

This module is a workflow guard, not a process sandbox. Callers must still
enforce the repository's ordinary ownership and permission boundaries.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import fcntl
from contextlib import contextmanager
import html
from pathlib import Path
import re
import tempfile
import argparse
import importlib.util
import sys
from datetime import datetime, timezone
from urllib.parse import unquote

VERDICTS = {"ACCEPTED", "CHANGES REQUIRED", "ESCALATE TO GUI"}
DISPOSITIONS = {"FIXED", "NOT APPLICABLE", "CANNOT FIX WITHIN SCOPE", "BLOCKED"}
DEFAULT_REVIEWER = {"model": "gpt-6.1-sol", "reasoning": "medium"}
REVIEW_DIMENSIONS = ("scope", "acceptance", "correctness", "regressions", "negative_cases",
                     "evidence", "validation", "plan_deviation", "complexity", "documentation",
                     "permissions", "limitations")
STATE_KEYS = {"version", "task_id", "parent_task_id", "contract", "contract_sha256", "result_path",
    "result_sha256", "changed_files", "executor_report", "executor_report_sha256", "handoff_binding",
    "executor_initial", "executor_initial_sha256",
    "executor", "reviews", "corrections", "review_artifacts", "correction_artifacts",
    "correction_authorizations", "correction_authorization_artifacts", "pending_corrections",
    "escalations", "escalation_artifacts", "executor_recoveries", "executor_recovery_artifacts",
    "cycle_triage", "cycle_triage_artifacts", "review_attempts", "review_attempt_artifacts",
    "gui_signals", "gui_signal_artifacts", "ready_for_gui", "escalation", "review_attempt_failures",
    "review_attempt_failure_artifacts"}


class ReviewError(ValueError):
    """Invalid, stale or conflicting review lifecycle evidence."""


def _check_task_id(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*", value):
        raise ReviewError("invalid task/handoff ID")


def _check_artifact_id(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Z][A-Z0-9-]{0,63}", value):
        raise ReviewError("invalid immutable artifact ID")


def _validate_identity(value, label):
    if value is not None and (not isinstance(value, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", value)):
        raise ReviewError(f"{label} must be a bounded opaque runtime identity or UNKNOWN")


def _validate_actual_profile(value, label):
    if value is None: return None
    if (not isinstance(value, dict) or set(value) != {"model", "reasoning"}
            or not isinstance(value["model"], str) or not value["model"].strip()
            or not isinstance(value["reasoning"], str) or value["reasoning"] not in {"low", "medium", "high", "xhigh", "max"}):
        raise ReviewError(f"{label} actual profile must be bounded or UNKNOWN")
    return value


def validate_routing(value, contract):
    """Validate the GUI-frozen, lightweight T-024 routing decision."""
    if value is None:
        return None  # legacy handoffs remain readable
    keys = {"execution_class", "review_route", "gui_finalization", "reason", "high_reason", "targeted_trigger"}
    if not isinstance(value, dict) or set(value) != keys:
        raise ReviewError("routing requires class, route, finalization, reason and explicit trigger fields")
    classes = {"MECHANICAL", "STANDARD", "COMPLEX", "DIAGNOSTIC"}
    routes = {"NONE", "SOL_MEDIUM", "SOL_HIGH", "DIAGNOSTIC"}
    finals = {"RECEIPT_ONLY", "TARGETED_REVIEW"}
    high = {"architecture_sensitive_correctness", "broad_shared_behavior_high_regression_cost",
            "unresolved_material_uncertainty_after_medium", "exceptional_quality_risk"}
    targeted = {"evidence_conflict", "missing_reviewer_provenance", "high_correction_count",
                "validation_gap", "material_shared_behavior", "reviewer_escalation",
                "receipt_inconsistency", "revision_mismatch", "manual_validation_pending",
                "explicit_direct_inspection"}
    if (not isinstance(value["execution_class"], str) or value["execution_class"] not in classes
            or not isinstance(value["review_route"], str) or value["review_route"] not in routes
            or not isinstance(value["gui_finalization"], str) or value["gui_finalization"] not in finals
            or not isinstance(value["reason"], str)
            or not value["reason"].strip() or len(value["reason"]) > 240):
        raise ReviewError("invalid T-024 routing classification")
    if (contract["review"]["profile"]["requested_reasoning"] in {"xhigh", "max"}
            or contract["execution"]["executor_profile"]["requested_reasoning"] in {"xhigh", "max"}):
        raise ReviewError("T-024 classification cannot automatically select XHigh/Max")
    if value["review_route"] == "SOL_HIGH":
        if (not isinstance(value["high_reason"], str) or value["high_reason"] not in high
                or contract["review"]["profile"]["requested_reasoning"] != "high"):
            raise ReviewError("Sol/High requires an allowed concrete reason and High reviewer profile")
        if not contract["loop"]["enabled"]:
            raise ReviewError("Sol/High requires the existing independent review path")
    elif value["high_reason"] is not None:
        raise ReviewError("High reason is valid only for the Sol/High route")
    if value["review_route"] == "SOL_MEDIUM" and (not contract["loop"]["enabled"]
            or contract["review"]["profile"]["requested_reasoning"] != "medium"):
        raise ReviewError("Sol/Medium requires the existing independent Medium review path")
    if value["review_route"] in {"NONE", "DIAGNOSTIC"} and contract["loop"]["enabled"]:
        raise ReviewError("no-review and diagnostic routes cannot enable the ordinary correction loop")
    if value["execution_class"] == "DIAGNOSTIC" and value["review_route"] != "DIAGNOSTIC":
        raise ReviewError("DIAGNOSTIC must reuse the existing diagnostic route")
    if value["review_route"] == "DIAGNOSTIC" and value["execution_class"] != "DIAGNOSTIC":
        raise ReviewError("diagnostic route requires DIAGNOSTIC classification")
    if value["gui_finalization"] == "TARGETED_REVIEW":
        if not isinstance(value["targeted_trigger"], str) or value["targeted_trigger"] not in targeted:
            raise ReviewError("TARGETED_REVIEW requires a concrete listed trigger")
    elif value["targeted_trigger"] is not None:
        raise ReviewError("targeted trigger is valid only for TARGETED_REVIEW")
    if value["execution_class"] == "MECHANICAL" and value["review_route"] in {"SOL_HIGH", "DIAGNOSTIC"}:
        raise ReviewError("MECHANICAL cannot automatically select High or diagnostic review")
    return value


def routing_summary(routing):
    summary = (f"{routing['execution_class']} · {routing['review_route']} · "
               f"GUI finalization {routing['gui_finalization']} · Reason: {routing['reason']}")
    if routing["high_reason"]:
        summary += " · High reason: " + routing["high_reason"].replace("_", " ").capitalize()
    return summary


@contextmanager
def _lifecycle_lock(root, task_id):
    _check_task_id(task_id)
    directory = Path(root).resolve(strict=True) / ".codex-sync" / "tasks" / task_id
    safe_root = Path(root).resolve(strict=True)
    _safe_file(safe_root, f".codex-sync/tasks/{task_id}/STATUS.json")
    _safe_file(safe_root, f".codex-sync/tasks/{task_id}/implementation-review/PENDING.json", exists=False)
    lock_path = directory / ".implementation-review.lock"
    if lock_path.is_symlink(): raise ReviewError("review lock symlink rejected")
    fd = os.open(lock_path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "a+") as stream:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
        try: yield
        finally: fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


@contextmanager
def _paired_lifecycle_lock(root, task_id):
    """Use the existing handoff lock first, then the immutable-cycle lock."""
    root = Path(root).resolve(strict=True)
    module_path = Path(__file__).resolve().with_name("handoff.py")
    spec = importlib.util.spec_from_file_location("handoff_shared_review_lock", module_path)
    if spec is None or spec.loader is None: raise ReviewError("handoff lock helper cannot be loaded")
    helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
    directory = helper.task_dir(root, task_id)
    with helper.locked(root, directory):
        with _lifecycle_lock(root, task_id):
            yield


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical(value) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def validate_cycle_telemetry(value):
    """Small factual T-021 attachment; never accepts transcript or hidden reasoning."""
    if value is None: return None
    required = {"cycle_role", "observation", "metrics", "usage_refs", "gui_context_ref"}
    if not isinstance(value, dict) or set(value) != required:
        raise ReviewError("cycle telemetry requires role/observation/metrics/usage_refs/gui_context_ref")
    if value["cycle_role"] not in {"executor", "reviewer", "correction", "gui"}:
        raise ReviewError("invalid telemetry cycle role")
    decoded_observation = value["observation"] if isinstance(value["observation"], str) else ""
    for _ in range(4):
        next_value = unquote(decoded_observation)
        if next_value == decoded_observation: break
        decoded_observation = next_value
    if (not isinstance(value["observation"], str) or len(value["observation"]) > 500
            or "transcript" in decoded_observation.lower()
            or re.search(r"(?i)(/Users/|/home/|/private/|[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}|session[_ -]?(?:id|key)?\s*[:=])", decoded_observation)):
        raise ReviewError("telemetry observation must be a short factual note")
    if not isinstance(value["metrics"], dict) or any(not isinstance(k, str) or (v is not None and (type(v) not in (int, float) or not math.isfinite(v) or v < 0)) for k, v in value["metrics"].items()):
        raise ReviewError("unknown telemetry metrics must be null; known metrics must be nonnegative numbers")
    for key in ("usage_refs", "gui_context_ref"):
        refs = value[key]
        if key == "usage_refs" and (not isinstance(refs, dict) or set(refs) - {"T-002", "other"}):
            raise ReviewError("usage refs may point to existing usage records only")
        if key == "gui_context_ref" and refs is not None and not isinstance(refs, str):
            raise ReviewError("GUI context must be a separate opaque reference or null")
        if isinstance(refs, dict) and any(v is not None and not isinstance(v, str) for v in refs.values()):
            raise ReviewError("usage refs must be opaque strings or null")
        values = [v for v in refs.values() if v is not None] if isinstance(refs, dict) else ([refs] if refs is not None else [])
        decoded_values = []
        for value_ref in values:
            decoded = value_ref
            for _ in range(4):
                nxt = unquote(decoded)
                if nxt == decoded: break
                decoded = nxt
            decoded_values.append(decoded)
        if any(not re.fullmatch(r"(?:usage|T-002|T-012|gui-context):[A-Z0-9][A-Z0-9._:-]{0,100}", v)
               or re.search(r"(?i)(/Users/|/home/|/private/|session[_ -]?(?:id|key)?\s*[:=])", v)
               for v in decoded_values):
            raise ReviewError("telemetry references must be bounded public identifiers, not paths or session IDs")
    return value


def _safe_file(root: Path, rel: str, *, exists=True) -> Path:
    p = Path(rel)
    if p.is_absolute() or not p.parts or ".." in p.parts or str(p) != rel:
        raise ReviewError("path must be normalized and repository-relative")
    cur = root
    for i, part in enumerate(p.parts):
        cur = cur / part
        if cur.is_symlink():
            raise ReviewError(f"symlink path rejected: {rel}")
        if i < len(p.parts) - 1 and cur.exists() and not cur.is_dir():
            raise ReviewError(f"non-directory path component: {rel}")
    if exists and not cur.is_file():
        raise ReviewError(f"missing regular file: {rel}")
    return cur


def _write_atomic(path: Path, data: bytes):
    fd, temp = tempfile.mkstemp(prefix=".review-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(temp, path)
    finally:
        if os.path.exists(temp): os.unlink(temp)


def _immutable_write(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    data = _canonical(value) + b"\n"
    try:
        with path.open("xb") as stream:
            stream.write(data); stream.flush(); os.fsync(stream.fileno())
    except FileExistsError as exc:
        raise ReviewError("immutable cycle artifact already exists") from exc
    return _sha(data)


def _transition_path(root: Path, task_id: str) -> Path:
    return _safe_file(root, f".codex-sync/tasks/{task_id}/implementation-review/PENDING.json", exists=False)


def _commit_transition(root: Path, task_id: str, state: dict, artifacts: list[tuple[str, dict]]):
    """Journal immutable artifact + projection writes for explicit crash recovery."""
    root = Path(root).resolve(strict=True)
    artifact_dir = root / ".codex-sync" / "tasks" / task_id / "implementation-review"
    _safe_file(root, f".codex-sync/tasks/{task_id}/implementation-review", exists=False)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    _safe_file(root, f".codex-sync/tasks/{task_id}/implementation-review", exists=False)
    projection = _safe_file(root, f".codex-sync/tasks/{task_id}/IMPLEMENTATION_REVIEW.json")
    pending = _transition_path(root, task_id)
    if pending.exists(): raise ReviewError("interrupted review transition pending; run recover-transition")
    before = projection.read_bytes()
    entries = []
    for kind, record in artifacts:
        data = _canonical(record) + b"\n"
        entries.append({"kind": kind, "id": record["id"], "record": record, "sha256": _sha(data)})
    journal = {"version": 1, "task_id": task_id, "before_sha256": _sha(before),
              "after_state": state, "after_sha256": _sha(_canonical(state) + b"\n"), "artifacts": entries}
    _write_atomic(pending, _canonical(journal) + b"\n")
    _finish_transition(root, task_id, journal)


def _finish_transition(root: Path, task_id: str, journal: dict):
    projection = _safe_file(root, f".codex-sync/tasks/{task_id}/IMPLEMENTATION_REVIEW.json")
    pending = _transition_path(root, task_id)
    for item in journal["artifacts"]:
        path = _immutable_path(root, task_id, item["kind"], item["id"])
        expected = _canonical(item["record"]) + b"\n"
        if _sha(expected) != item["sha256"]: raise ReviewError("transition journal artifact hash mismatch")
        if path.exists():
            if path.read_bytes() != expected: raise ReviewError("immutable artifact conflicts with interrupted transition")
        else:
            actual = _immutable_write(path, item["record"])
            if actual != item["sha256"]: raise ReviewError("immutable artifact write hash mismatch")
    current = projection.read_bytes()
    if _sha(current) == journal["before_sha256"]:
        _write_atomic(projection, _canonical(journal["after_state"]) + b"\n")
    elif _sha(current) != journal["after_sha256"]:
        raise ReviewError("review projection changed during interrupted transition")
    pending.unlink()


def recover_transition(root, task_id: str):
    """Explicitly finish one exact journaled artifact/projection transition."""
    root = Path(root).resolve(strict=True)
    with _paired_lifecycle_lock(root, task_id):
        pending = _transition_path(root, task_id)
        if not pending.exists(): raise ReviewError("there is no interrupted review transition")
        try: journal = json.loads(pending.read_text(encoding="utf-8"))
        except (ValueError, UnicodeError) as exc: raise ReviewError("invalid interrupted transition journal") from exc
        if (not isinstance(journal, dict) or set(journal) != {"version", "task_id", "before_sha256", "after_state", "after_sha256", "artifacts"}
                or journal["version"] != 1 or journal["task_id"] != task_id or not isinstance(journal["artifacts"], list)
                or not re.fullmatch(r"[0-9a-f]{64}", str(journal["before_sha256"]))
                or not re.fullmatch(r"[0-9a-f]{64}", str(journal["after_sha256"]))
                or not isinstance(journal["after_state"], dict)):
            raise ReviewError("interrupted transition journal identity/shape mismatch")
        for item in journal["artifacts"]:
            if (not isinstance(item, dict) or set(item) != {"kind", "id", "record", "sha256"}
                    or item["kind"] not in {"cycle_triage", "correction_authorizations", "escalations", "executor_recoveries",
                        "review_attempts", "review_attempt_failures", "reviews", "corrections", "gui_signals"}
                    or not isinstance(item["record"], dict) or item["record"].get("id") != item["id"]
                    or not re.fullmatch(r"[0-9a-f]{64}", str(item["sha256"]))):
                raise ReviewError("interrupted transition artifact entry is invalid")
        projection = _safe_file(root, f".codex-sync/tasks/{task_id}/IMPLEMENTATION_REVIEW.json")
        current = projection.read_bytes()
        if _sha(current) not in {journal["before_sha256"], journal["after_sha256"]}:
            raise ReviewError("interrupted transition no longer matches current projection")
        try: _verify_handoff_binding(root, json.loads(current.decode("utf-8")))
        except (ValueError, UnicodeError) as exc: raise ReviewError("current lifecycle cannot bind to its handoff") from exc
        _finish_transition(root, task_id, journal)
        _load(root, task_id)
        _write_final_receipt(root, task_id)
        return journal["after_state"]


def _immutable_path(root: Path, task_id: str, kind: str, artifact_id: str):
    _check_task_id(task_id); _check_artifact_id(artifact_id)
    rel = f".codex-sync/tasks/{task_id}/implementation-review/{kind}/{artifact_id}.json"
    path = _safe_file(root, rel, exists=False)
    if not path.parent.is_dir():
        path.parent.mkdir(parents=True, exist_ok=True)
        _safe_file(root, rel, exists=False)
    return path


def validate_contract(contract: dict) -> dict:
    """Validate the paired, GUI-frozen execution/review contract."""
    required = {"version", "task_id", "revision", "execution", "review", "loop"}
    if not isinstance(contract, dict) or frozenset(contract) not in {frozenset(required), frozenset(required | {"routing"})} or type(contract["version"]) is not int or contract["version"] not in {1, 2}:
        raise ReviewError("contract requires version/task_id/revision/execution/review/loop")
    if not isinstance(contract["task_id"], str) or not re.fullmatch(r"[A-Z0-9][A-Z0-9-]{1,63}", contract["task_id"]):
        raise ReviewError("invalid task identity")
    if type(contract["revision"]) is not int or contract["revision"] < 1:
        raise ReviewError("invalid frozen revision")
    execution, review, loop = contract["execution"], contract["review"], contract["loop"]
    if not isinstance(execution, dict) or not isinstance(review, dict) or not isinstance(loop, dict):
        raise ReviewError("execution, review and loop must be objects")
    if not all(isinstance(execution.get(k), str) and execution[k].strip() for k in ("scope", "acceptance", "permissions", "invariants")):
        raise ReviewError("execution contract requires scope, acceptance, invariants and permissions")
    if not isinstance(execution.get("inputs"), list) or not 1 <= len(execution["inputs"]) <= 100:
        raise ReviewError("paired execution contract requires a bounded named input list")
    for rel in execution["inputs"]:
        p = Path(rel) if isinstance(rel, str) else Path("/")
        if p.is_absolute() or ".." in p.parts or not p.parts or str(p) != rel:
            raise ReviewError("contract input paths must be normalized and repository-relative")
    plan = execution.get("plan_of_execution")
    if not isinstance(plan, list) or not 1 <= len(plan) <= 10 or any(not isinstance(x, str) or not x.strip() or len(x) > 200 for x in plan):
        raise ReviewError("frozen human-readable plan requires 1–10 concise bullets")
    if not re.fullmatch(r"[0-9a-f]{64}", str(execution.get("plan_summary_sha256", ""))):
        raise ReviewError("paired contract must bind the frozen handoff plan summary")
    executor = execution.get("executor_profile")
    if (not isinstance(executor, dict) or set(executor) != {"requested_model", "requested_reasoning", "justification"}
            or not isinstance(executor["requested_model"], str) or not executor["requested_model"].strip()
            or executor["requested_reasoning"] not in {"low", "medium", "high", "xhigh", "max"}
            or not isinstance(executor["justification"], str) or not executor["justification"].strip()):
        raise ReviewError("executor profile must be explicitly selected and justified")
    if not isinstance(execution.get("validation"), list) or not execution["validation"] or any(not isinstance(x, str) or not x.strip() for x in execution["validation"]):
        raise ReviewError("named validation requirements are required")
    if not isinstance(review.get("dimensions"), list) or set(review["dimensions"]) != set(REVIEW_DIMENSIONS):
        raise ReviewError("review contract must freeze all named review dimensions")
    budget = review.get("budget")
    if (not isinstance(budget, dict) or set(budget) != {"max_changed_files", "max_evidence_items"}
            or any(type(v) is not int or not 1 <= v <= 1000 for v in budget.values())):
        raise ReviewError("review contract must set bounded changed-file and evidence budgets")
    profile = review.get("profile")
    if (not isinstance(profile, dict) or set(profile) != {"requested_model", "requested_reasoning", "justification"}
            or not profile["requested_model"] or profile["requested_reasoning"] not in {"medium", "high", "xhigh", "max"}
            or not isinstance(profile["justification"], str)):
        raise ReviewError("reviewer profile must be GUI-selected and explicit")
    expected_loop = {"enabled", "correction_budget", "budget_rationale", "escalation"} if contract["version"] == 1 else {"enabled", "correction_policy", "correction_budget", "budget_rationale", "escalation"}
    if set(loop) != expected_loop or type(loop["enabled"]) is not bool:
        raise ReviewError("invalid loop configuration")
    policy = loop.get("correction_policy", "MAX_CYCLES")
    if loop["enabled"] and (not isinstance(policy, str) or policy not in {"MAX_CYCLES", "UNTIL_ACCEPTED_OR_ESCALATED"}
                             or (policy == "MAX_CYCLES" and (type(loop["correction_budget"]) is not int or loop["correction_budget"] < 1))
                             or (policy == "UNTIL_ACCEPTED_OR_ESCALATED" and loop["correction_budget"] is not None)
                             or not isinstance(loop["budget_rationale"], str) or not loop["budget_rationale"].strip()):
        raise ReviewError("enabled loop requires an explicit valid correction policy and consistent budget")
    if not loop["enabled"] and (loop["correction_budget"] is not None or loop["budget_rationale"] is not None):
        raise ReviewError("disabled loop cannot declare a correction budget")
    if not isinstance(loop["escalation"], str) or not loop["escalation"].strip():
        raise ReviewError("escalation rules are required")
    validate_routing(contract.get("routing"), contract)
    return contract


def _handoff_snapshot(root: Path, task_id: str, contract: dict, result_path: str,
                      result_hash: str, changed_files: dict) -> dict:
    """Bind review initialization to the completed registered handoff record."""
    status_rel = f".codex-sync/tasks/{task_id}/STATUS.json"
    contract_rel = f".codex-sync/tasks/{task_id}/IMPLEMENTATION_REVIEW_CONTRACT.json"
    status = _load_payload(root, status_rel)
    _validate_registered_handoff(root, task_id, status)
    contract_file = _safe_file(root, contract_rel)
    raw_contract = contract_file.read_bytes()
    try:
        frozen_contract = json.loads(raw_contract.decode("utf-8"))
    except (ValueError, UnicodeError) as exc:
        raise ReviewError("frozen handoff review contract is invalid") from exc
    if frozen_contract != contract or _sha(raw_contract) != status.get("review_contract_sha256"):
        raise ReviewError("review contract differs from the handoff's frozen paired contract")
    if status.get("id") != task_id or status.get("parent_id") != contract["task_id"]:
        raise ReviewError("review identity differs from the registered handoff")
    if status.get("status") != "COMPLETED":
        raise ReviewError("review initialization requires the current completed handoff")
    expected_result = f".codex-sync/tasks/{task_id}/CLI_RESULT.md"
    if result_path != expected_result or status.get("result_sha256") != result_hash:
        raise ReviewError("review result path/hash differs from the current completed handoff")
    if status.get("review_contract_scope_sha256") != status.get("scope_sha256"):
        raise ReviewError("paired review contract is not bound to the frozen execution description")
    outputs = status.get("outputs")
    if not isinstance(outputs, dict) or any(outputs.get(rel) != digest for rel, digest in changed_files.items()):
        raise ReviewError("reviewed changed-file inventory differs from completed handoff outputs")
    expected_changed = {rel for rel in status.get("owned", []) if outputs.get(rel) != status.get("inputs", {}).get(rel)}
    if set(changed_files) != expected_changed:
        raise ReviewError("review changed-file list must exactly match changed owned outputs")
    if not set(changed_files).issubset(set(status.get("owned", []))):
        raise ReviewError("reviewed file is outside the handoff's frozen owned paths")
    return {key: status.get(key) for key in ("id", "parent_id", "attempt", "revision", "owner", "scope_sha256",
            "review_contract_sha256", "review_contract_scope_sha256", "inputs", "owned", "outputs", "result_sha256")}


def _verify_handoff_binding(root: Path, state: dict) -> tuple[dict, bool]:
    """Verify immutable handoff identity and whether its latest result is current."""
    binding = state.get("handoff_binding")
    if not isinstance(binding, dict):
        raise ReviewError("lifecycle is not bound to a registered completed handoff")
    status = _load_payload(root, f".codex-sync/tasks/{state['task_id']}/STATUS.json")
    _validate_registered_handoff(root, state["task_id"], status)
    frozen_path = _safe_file(root, f".codex-sync/tasks/{state['task_id']}/IMPLEMENTATION_REVIEW_CONTRACT.json")
    frozen_raw = frozen_path.read_bytes()
    try: frozen_contract = json.loads(frozen_raw.decode("utf-8"))
    except (ValueError, UnicodeError) as exc: raise ReviewError("frozen paired contract is invalid") from exc
    if (_sha(frozen_raw) != status.get("review_contract_sha256") or frozen_contract != state.get("contract")
            or _sha(_canonical(frozen_contract)) != state.get("contract_sha256")):
        raise ReviewError("effective paired contract differs from exact registered frozen contract")
    for key in ("id", "parent_id", "attempt", "owner", "scope_sha256", "review_contract_sha256",
                "review_contract_scope_sha256", "inputs", "owned"):
        if status.get(key) != binding.get(key):
            raise ReviewError(f"registered handoff immutable binding changed: {key}")
    if type(status.get("revision")) is not int or status["revision"] < binding["revision"]:
        raise ReviewError("registered handoff revision moved backwards")
    correction_id = status.get("implementation_review_correction_id")
    if status.get("status") == "IN_PROGRESS":
        authorized = state.get("pending_corrections", {}).get(correction_id)
        if authorized is None or not state.get("reviews") or authorized.get("source_review") != state["reviews"][-1]["id"]:
            raise ReviewError("handoff correction re-entry is not bound to a current correction package")
        return status, False
    if status.get("status") not in {"COMPLETED", "CONSUMED"}:
        raise ReviewError("handoff is neither in an authorized correction nor a completed state")
    pending = state.get("pending_corrections", {}).get(correction_id)
    if pending is not None:
        return status, False
    if status.get("result_sha256") != state.get("result_sha256"):
        raise ReviewError("review lifecycle result differs from current completed handoff result")
    expected_changed = {rel for rel in status.get("owned", [])
                        if status.get("outputs", {}).get(rel) != status.get("inputs", {}).get(rel)}
    if expected_changed != set(state.get("changed_files", {})):
        raise ReviewError("review changed-file inventory differs from all changed owned outputs")
    for rel, digest in state.get("changed_files", {}).items():
        if status.get("outputs", {}).get(rel) != digest:
            raise ReviewError("review lifecycle changed-file hashes differ from current handoff outputs")
    return status, True


def _validate_registered_handoff(root: Path, task_id: str, status: dict):
    """Run the handoff's own frozen-scope, registry and input-integrity checks."""
    module_path = Path(__file__).resolve().with_name("handoff.py")
    spec = importlib.util.spec_from_file_location("paired_review_handoff_validator", module_path)
    if spec is None or spec.loader is None: raise ReviewError("registered handoff validator cannot be loaded")
    helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
    directory = root / ".codex-sync" / "tasks" / task_id
    try: helper.contract(root, directory, status)
    except (helper.HandoffError, ValueError, OSError) as exc: raise ReviewError(f"registered handoff frozen inputs failed validation: {exc}") from exc


def _execution_review(root, result_path):
    module_path = Path(__file__).resolve().with_name("execution_review.py")
    spec = importlib.util.spec_from_file_location("execution_review_cycle_adapter", module_path)
    if spec is None or spec.loader is None: raise ReviewError("T-021 report validator cannot be loaded")
    helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
    text = _safe_file(root, result_path).read_text(encoding="utf-8")
    report = helper.extract_review(text)
    helper.validate_review(report)
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    return report, _sha(canonical)


def _telemetry_report(telemetry, role):
    telemetry = validate_cycle_telemetry(telemetry)
    categories = {name: "NONE" for name in (
        "errors_recovery", "execution_time", "token_context_hotspots", "rework",
        "automation_candidates", "discovery_overhead", "repeated_knowledge_acquisition",
        "validation_gaps", "scope_process_anomalies")}
    if telemetry:
        target = {"executor": "errors_recovery", "reviewer": "validation_gaps",
                  "correction": "rework", "gui": "scope_process_anomalies"}[role]
        categories[target] = telemetry["observation"]
        metrics = telemetry["metrics"]
        elapsed = metrics.get("elapsed_seconds", metrics.get("time_seconds"))
        tokens = metrics.get("tokens")
    else:
        elapsed = tokens = None
    return {"type": "post_execution_self_review", "version": 1, "categories": categories,
            "cost_hotspots": [], "metrics": {"elapsed_seconds": elapsed, "tokens": tokens}}


def cycle_reports(root, task_id):
    """Return deterministic T-021 reports for the executor and every review/correction cycle."""
    root, _, state = _load(root, task_id)
    reports = []
    initial = state["executor_report"]
    reports.append({"cycle_id": "EXEC-1", "role": "executor", "report": initial,
                    "report_sha256": state["executor_report_sha256"]})
    for item in state["reviews"]:
        report = _telemetry_report(item.get("telemetry"), "reviewer")
        canonical = _canonical(report)
        reports.append({"cycle_id": f"REVIEW-{item['id']}", "role": "reviewer", "report": report, "report_sha256": _sha(canonical)})
    for item in state["corrections"]:
        report = _telemetry_report(item.get("telemetry"), "correction")
        reports.append({"cycle_id": f"CORRECTION-{item['id']}", "role": "correction", "report": report,
                        "report_sha256": _sha(_canonical(report))})
        executor_report = item["executor_report"]
        reports.append({"cycle_id": f"EXEC-{item['id']}", "role": "executor", "report": executor_report,
                        "report_sha256": item["executor_report_sha256"]})
    for item in state.get("gui_signals", []):
        report = _telemetry_report({"cycle_role": "gui", "observation": item["reason"],
            "metrics": {"elapsed_seconds": None, "tokens": None}, "usage_refs": {}, "gui_context_ref": None}, "gui")
        reports.append({"cycle_id": item["id"], "role": "gui", "report": report,
                        "report_sha256": _sha(_canonical(report))})
    for item in state.get("escalations", []):
        report = _telemetry_report({"cycle_role": "gui", "observation": item["reason"],
            "metrics": {"elapsed_seconds": None, "tokens": None}, "usage_refs": {}, "gui_context_ref": None}, "gui")
        reports.append({"cycle_id": item["id"], "role": "gui", "report": report,
                        "report_sha256": _sha(_canonical(report))})
    for item in state.get("executor_recoveries", []):
        report = _telemetry_report({"cycle_role": "executor", "observation": item["reason"],
            "metrics": {"elapsed_seconds": None, "tokens": None}, "usage_refs": {}, "gui_context_ref": None}, "executor")
        reports.append({"cycle_id": item["id"], "role": "executor", "report": report,
                        "report_sha256": _sha(_canonical(report))})
    return reports


def render_final_receipt(root, task_id):
    root, _, state = _load(root, task_id)
    status = _load_payload(root, f".codex-sync/tasks/{task_id}/STATUS.json")
    latest = state["reviews"][-1] if state["reviews"] else None
    final_profile = (latest or {}).get("actual_profile") or "UNKNOWN / unverified"
    executor_profile = state.get("executor", {}).get("actual_profile") or "UNKNOWN / unverified"
    lines = ["FINAL RECEIPT", "", f"Task: {task_id} (parent {state['parent_task_id']})",
        f"Execution result: {'COMPLETE' if status.get('status') in {'COMPLETED', 'CONSUMED'} else status.get('status')}",
        f"Current result SHA-256: {status.get('result_sha256')}",
        f"Executor requested / actual profile: {state['executor'].get('requested_profile')} / {executor_profile}",
        f"Independent review: {latest.get('verdict') if latest else 'PENDING'}",
        f"Final reviewer profile: {final_profile}",
        f"Correction policy: {state['contract']['loop'].get('correction_policy', 'MAX_CYCLES')}",
        f"Maximum corrections: {state['contract']['loop']['correction_budget'] if state['contract']['loop'].get('correction_policy', 'MAX_CYCLES') == 'MAX_CYCLES' else 'NONE'}",
        f"Review count: {len(state['reviews'])}", f"Correction-cycle count: {len(state['corrections'])}", "",
        f"Executor continuity breaks: {len(state.get('executor_recoveries', []))}",
        "Findings summary by cycle:"]
    routing = state["contract"].get("routing")
    if routing:
        lines.insert(3, "Routing: " + routing_summary(routing))
    if not state["reviews"]: lines.append("- No reviews recorded.")
    for index, item in enumerate(state["reviews"]):
        findings = item.get("findings", []) + item.get("escalated_findings", [])
        lines.append(f"- {item['id']}: {item['verdict']}; {len(findings)} finding(s).")
        for finding in findings:
            disposition = next((c.get("dispositions", {}).get(finding["id"]) for c in state["corrections"]
                                if c.get("source_review") == item["id"]), None)
            next_review = state["reviews"][index + 1] if index + 1 < len(state["reviews"]) else None
            resolution = (next_review or {}).get("resolutions", {}).get(finding["id"])
            reviewer_status = resolution.get("status") if resolution else "PENDING"
            executor_status = disposition.get("disposition") if disposition else "NONE"
            lines.append(f"  - {finding['id']} [{finding['severity']}] reviewer: {reviewer_status}; executor claim: {executor_status}: {finding['criterion']}")
    final_findings = {}
    for item in state["reviews"]:
        for finding_id, outcome in item.get("resolutions", {}).items():
            if finding_id in final_findings:
                final_findings[finding_id] = {**final_findings[finding_id],
                    "status": outcome["status"],
                    "evidence": outcome["evidence"]}
        for finding in item.get("findings", []) + item.get("escalated_findings", []):
            final_findings[finding["id"]] = {"finding": finding, "status": "OPEN", "evidence": ""}
    for item in state.get("escalations", []):
        for finding in item.get("carried_findings", []):
            entry = final_findings.setdefault(finding["id"], {"finding": finding, "status": "OPEN", "evidence": ""})
            entry["status"] = "ESCALATED"
            entry["evidence"] = item.get("reason", "")
    lines += ["", "Final disposition by material finding:"]
    if not final_findings:
        lines.append("- None recorded.")
    for finding_id, entry in sorted(final_findings.items()):
        finding = entry["finding"]
        lines.append(f"- {finding_id}: {entry['status']}; {finding['criterion']}; evidence: {entry['evidence'] or 'UNKNOWN'}")
    result_text = _safe_file(root, f".codex-sync/tasks/{task_id}/CLI_RESULT.md").read_text(encoding="utf-8")
    lines += ["", "Required execution checks:"]
    for check in status.get("required_checks", []):
        matches = re.findall(r"(?m)^- " + re.escape(check) + r": (PASS|FAIL)$", result_text)
        lines.append(f"- {check}: {matches[0] if len(matches) == 1 else 'UNKNOWN / invalid receipt line'}")
    lines.append("Unverified runtime/manual validation: UNKNOWN unless separate evidence is attached.")
    lines.append("Independent reviewer dimensions:")
    if latest:
        lines.extend(f"- {name}: {result}" for name, result in latest.get("dimensions", {}).items())
    else: lines.append("- No independent validation recorded.")
    lines += ["", "Current owned outputs:"]
    lines.extend(f"- {rel} sha256:{digest}" for rel, digest in sorted(status.get("outputs", {}).items()))
    lines += ["", "T-021 cycle report hashes:"]
    triaged = {item["cycle_id"]: item["report_sha256"] for item in state.get("cycle_triage", [])}
    lines.extend(f"- {item['cycle_id']} sha256:{item['report_sha256']} — {'GUI triaged' if triaged.get(item['cycle_id']) == item['report_sha256'] else 'PENDING'}"
                 for item in cycle_reports(root, task_id))
    cycle_metrics = [item["report"].get("metrics", {}) for item in cycle_reports(root, task_id)]
    known_elapsed = [m["elapsed_seconds"] for m in cycle_metrics if type(m.get("elapsed_seconds")) in {int, float}]
    known_tokens = [m["tokens"] for m in cycle_metrics if type(m.get("tokens")) is int]
    lines += [f"Scope drift: {'NONE; frozen handoff scope and contract hashes match' if status.get('scope_sha256') == state['handoff_binding'].get('scope_sha256') else 'DETECTED'}",
        "Validation gaps / manual checks still required: UNKNOWN unless recorded in the current handoff result.",
        "Post-execution self-review: initial report and per-correction reports are available as bounded cycle attachments.",
        f"T-021 optimization-inventory ingestion: {len(state.get('cycle_triage', []))}/{len(cycle_reports(root, task_id))} cycle reports triaged.",
        f"Known cycle elapsed aggregate (seconds): {sum(known_elapsed) if known_elapsed else 'UNKNOWN'}; measured {len(known_elapsed)}/{len(cycle_metrics)}.",
        f"Known cycle token aggregate: {sum(known_tokens) if known_tokens else 'UNKNOWN'}; measured {len(known_tokens)}/{len(cycle_metrics)}.",
        f"AI/token telemetry references: {state['executor_report'].get('metrics', {})}; unknown remains null.",
        f"GUI-context telemetry reference: {state['contract']['execution'].get('gui_context_ref', 'UNKNOWN')}.",
        f"Final repository/task revision: handoff attempt {status['attempt']} revision {status['revision']}."]
    current_escalation = next((e.get("reason") for e in reversed(state.get("escalations", []))
                               if latest and e.get("source_review") == latest["id"]
                               and state.get("escalation_artifacts", {}).get(e.get("id"))), None)
    if current_escalation:
        lines += ["", "Escalation: " + current_escalation]
    loop = state["contract"]["loop"]
    lines += [f"Correction policy: {loop.get('correction_policy', 'MAX_CYCLES')}",
              f"Maximum corrections: {loop['correction_budget'] if loop.get('correction_policy', 'MAX_CYCLES') == 'MAX_CYCLES' else 'NONE'}",
              f"First-pass acceptance: {('YES' if state['reviews'][0]['verdict'] == 'ACCEPTED' else 'NO') if state['reviews'] else 'UNKNOWN'}"]
    findings_by_id = {}
    for cycle in state["reviews"]:
        for finding in cycle.get("findings", []) + cycle.get("escalated_findings", []):
            findings_by_id[finding["id"]] = findings_by_id.get(finding["id"], 0) + 1
    lines.append("Repeated finding occurrences: " + str(sum(max(0, n - 1) for n in findings_by_id.values())))
    gui_rejection = next((x for x in reversed(state.get("gui_signals", []))
                          if x.get("type") == "gui_acceptance_rejected"), None)
    lines.append("GUI acceptance quality signal: " + ("REJECTED — " + gui_rejection["reason"] if gui_rejection else "NONE RECORDED"))
    return "\n".join(lines) + "\n"


def _write_final_receipt(root, task_id, state=None):
    text = render_final_receipt(root, task_id)
    path = _safe_file(Path(root).resolve(strict=True), f".codex-sync/tasks/{task_id}/IMPLEMENTATION_REVIEW_FINAL_RECEIPT.md", exists=False)
    if path.exists():
        if path.read_text(encoding="utf-8") == text: return path
    _write_atomic(path, text.encode("utf-8"))
    return path


def require_final_receipt(root, task_id):
    path = _safe_file(Path(root).resolve(strict=True), f".codex-sync/tasks/{task_id}/IMPLEMENTATION_REVIEW_FINAL_RECEIPT.md")
    if path.read_text(encoding="utf-8") != render_final_receipt(root, task_id):
        raise ReviewError("final GUI receipt is stale or differs from deterministic lifecycle evidence")
    return True


def record_cycle_triage(root, task_id: str, *, cycle_id: str, inventory_path, actor: str):
    """Persist GUI's confirmation that a cycle report has a T-021 ledger entry."""
    if actor != "GUI": raise ReviewError("cycle triage confirmation is GUI-owned")
    inventory_path = Path(inventory_path)
    with _paired_lifecycle_lock(root, task_id):
        root, path, state = _load(root, task_id)
        report = next((x for x in cycle_reports(root, task_id) if x["cycle_id"] == cycle_id), None)
        if report is None: raise ReviewError("unknown cycle report")
        er_path = Path(__file__).resolve().with_name("execution_review.py")
        spec = importlib.util.spec_from_file_location("execution_review_triage_check", er_path)
        helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
        try: data = helper._read_inventory(inventory_path)
        except (ValueError, OSError) as exc: raise ReviewError(f"T-021 inventory validation failed: {exc}") from exc
        status = _load_payload(root, f".codex-sync/tasks/{task_id}/STATUS.json")
        identity = f"{task_id}:{status['attempt']}:{cycle_id}"
        entry = next((x for x in data["ledger"] if x.get("identity") == identity), None)
        if entry is None or entry.get("report_sha256") != report["report_sha256"]:
            raise ReviewError("cycle report is not ingested into T-021 with its exact report hash")
        record = {"id": cycle_id, "cycle_id": cycle_id, "report_sha256": report["report_sha256"],
                  "ledger_identity": identity, "ledger_id": entry["id"], "actor": actor,
                  "created_at": datetime.now(timezone.utc).isoformat()}
        previous = next((x for x in state.get("cycle_triage", []) if x["cycle_id"] == cycle_id), None)
        if previous:
            if any(previous.get(key) != record.get(key) for key in ("cycle_id", "report_sha256", "ledger_identity", "ledger_id", "actor")):
                raise ReviewError("cycle triage confirmation conflicts with its immutable receipt")
            return previous
        artifact_hash = _sha(_canonical(record) + b"\n")
        state.setdefault("cycle_triage", []).append(record)
        state.setdefault("cycle_triage_artifacts", {})[cycle_id] = artifact_hash
        _commit_transition(root, task_id, state, [("cycle_triage", record)])
        _write_final_receipt(root, task_id, state)
        return record


def require_cycle_triage(root, task_id):
    state = _load(root, task_id)[2]
    expected = {r["cycle_id"]: r["report_sha256"] for r in cycle_reports(root, task_id)}
    actual = {r["cycle_id"]: r["report_sha256"] for r in state.get("cycle_triage", [])}
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        stale = sorted(c for c in set(actual) & set(expected) if actual[c] != expected[c])
        raise ReviewError(f"GUI must triage every current T-021 cycle report; missing={missing}, stale={stale}")
    return True


def initialize(root, task_id: str, contract: dict, *, result_path: str, changed_paths: list[str],
               executor_identity: str | None = None, executor_actual_profile: dict | None = None):
    """Freeze paired contracts and exact result/diff input references."""
    root = Path(root).resolve(strict=True)
    with _paired_lifecycle_lock(root, task_id):
        return _initialize_locked(root, task_id, contract, result_path=result_path,
            changed_paths=changed_paths, executor_identity=executor_identity,
            executor_actual_profile=executor_actual_profile)


def _initialize_locked(root, task_id, contract, *, result_path, changed_paths,
                       executor_identity=None, executor_actual_profile=None):
    _check_task_id(task_id)
    validate_contract(contract)
    _validate_identity(executor_identity, "executor")
    _validate_actual_profile(executor_actual_profile, "executor")
    result = _safe_file(root, result_path)
    files = {}
    for rel in sorted(set(changed_paths)):
        p = _safe_file(root, rel)
        files[rel] = _sha(p.read_bytes())
    binding = _handoff_snapshot(root, task_id, contract, result_path, _sha(result.read_bytes()), files)
    executor_report, executor_report_sha = _execution_review(root, result_path)
    initial_executor = {"id": "INITIAL", "identity": executor_identity,
        "requested_profile": contract["execution"]["executor_profile"],
        "actual_profile": executor_actual_profile, "result_path": result_path,
        "result_sha256": _sha(result.read_bytes()), "report": executor_report,
        "report_sha256": executor_report_sha}
    initial_bytes = _canonical(initial_executor) + b"\n"
    initial_path = _safe_file(root, f".codex-sync/tasks/{task_id}/implementation-review/executor_initial/INITIAL.json", exists=False)
    if initial_path.exists():
        if initial_path.read_bytes() != initial_bytes:
            raise ReviewError("existing immutable initial executor snapshot conflicts with initialization")
        initial_hash = _sha(initial_bytes)
    else:
        initial_hash = _immutable_write(initial_path, initial_executor)
    state = {"version": 1, "task_id": task_id, "parent_task_id": contract["task_id"], "contract": contract,
             "contract_sha256": _sha(_canonical(contract)), "result_path": result_path,
             "result_sha256": _sha(result.read_bytes()), "changed_files": files,
             "executor_report": executor_report, "executor_report_sha256": executor_report_sha,
             "executor_initial": initial_executor, "executor_initial_sha256": initial_hash,
             "handoff_binding": binding,
             "executor": {"requested_profile": contract["execution"]["executor_profile"], "actual_profile": executor_actual_profile,
                          "identity": executor_identity, "initial_identity": executor_identity,
                          "initial_actual_profile": executor_actual_profile},
             "reviews": [], "corrections": [], "review_artifacts": {}, "correction_artifacts": {},
             "correction_authorizations": [], "correction_authorization_artifacts": {}, "pending_corrections": {},
             "escalations": [], "escalation_artifacts": {}, "executor_recoveries": [], "executor_recovery_artifacts": {},
             "cycle_triage": [], "cycle_triage_artifacts": {},
             "review_attempts": [], "review_attempt_artifacts": {},
             "review_attempt_failures": [], "review_attempt_failure_artifacts": {},
             "gui_signals": [], "gui_signal_artifacts": {},
             "ready_for_gui": False, "escalation": None}
    path = root / ".codex-sync" / "tasks" / task_id / "IMPLEMENTATION_REVIEW.json"
    if path.exists() or path.is_symlink():
        raise ReviewError("review lifecycle already exists")
    if not path.parent.is_dir(): raise ReviewError("task directory is missing")
    _write_atomic(path, _canonical(state) + b"\n")
    return state


def _load(root, task_id):
    _check_task_id(task_id)
    root = Path(root).resolve(strict=True)
    rel = f".codex-sync/tasks/{task_id}/IMPLEMENTATION_REVIEW.json"
    pending = _safe_file(root, f".codex-sync/tasks/{task_id}/implementation-review/PENDING.json", exists=False)
    if pending.exists(): raise ReviewError("interrupted review transition pending; run recover-transition")
    path = _safe_file(root, rel)
    try: state = json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as exc: raise ReviewError("invalid lifecycle JSON") from exc
    if isinstance(state, dict) and ("executor_initial" not in state or "executor_initial_sha256" not in state):
        raise ReviewError("historical lifecycle lacks an immutable initial executor snapshot; GUI migration decision required")
    if (not isinstance(state, dict) or set(state) != STATE_KEYS
            or type(state.get("version")) is not int or state.get("version") != 1
            or any(not isinstance(state.get(key), list) for key in ("reviews", "corrections", "correction_authorizations",
                "escalations", "executor_recoveries", "cycle_triage", "review_attempts", "review_attempt_failures", "gui_signals"))
            or any(not isinstance(state.get(key), dict) for key in ("review_artifacts", "correction_artifacts",
                "correction_authorization_artifacts", "pending_corrections", "escalation_artifacts",
                "executor_recovery_artifacts", "cycle_triage_artifacts", "review_attempt_artifacts",
                "review_attempt_failure_artifacts", "gui_signal_artifacts", "changed_files", "executor"))
            or type(state.get("ready_for_gui")) is not bool):
        raise ReviewError("lifecycle projection has invalid or unsupported structure")
    validate_contract(state.get("contract"))
    if state.get("task_id") != task_id or state.get("parent_task_id") != state["contract"].get("task_id") or _sha(_canonical(state["contract"])) != state.get("contract_sha256"):
        raise ReviewError("lifecycle identity/contract tampering")
    _verify_handoff_binding(root, state)
    initial = state.get("executor_initial")
    if not isinstance(initial, dict):
        raise ReviewError("historical lifecycle lacks an immutable initial executor snapshot; GUI migration decision required")
    if set(initial) != {"id", "identity", "requested_profile", "actual_profile", "result_path", "result_sha256", "report", "report_sha256"}:
        raise ReviewError("immutable initial executor snapshot has an invalid structure")
    initial_path = _safe_file(root, f".codex-sync/tasks/{task_id}/implementation-review/executor_initial/INITIAL.json")
    initial_raw = initial_path.read_bytes()
    if (_sha(initial_raw) != state.get("executor_initial_sha256")
            or json.loads(initial_raw.decode("utf-8")) != initial
            or initial.get("id") != "INITIAL"
            or initial.get("identity") != state["executor"].get("initial_identity")
            or initial.get("requested_profile") != state["contract"]["execution"]["executor_profile"]
            or state["executor"].get("requested_profile") != initial.get("requested_profile")
            or initial.get("actual_profile") != state["executor"].get("initial_actual_profile")
            or state["executor"].get("actual_profile") != initial.get("actual_profile")
            or initial.get("result_path") != f".codex-sync/tasks/{task_id}/CLI_RESULT.md"
            or initial.get("result_sha256") != state.get("handoff_binding", {}).get("result_sha256")
            or initial.get("report") != state.get("executor_report")
            or initial.get("report_sha256") != state.get("executor_report_sha256")
            or initial.get("report_sha256") != _sha(_canonical(initial.get("report")))):
        raise ReviewError("immutable initial executor authority does not match its lifecycle projection")
    for kind, collection, hashes in (("reviews", state["reviews"], state.get("review_artifacts", {})),
                                     ("corrections", state["corrections"], state.get("correction_artifacts", {})),
                                     ("correction_authorizations", state.get("correction_authorizations", []), state.get("correction_authorization_artifacts", {})),
                                     ("review_attempts", state.get("review_attempts", []), state.get("review_attempt_artifacts", {})),
                                     ("gui_signals", state.get("gui_signals", []), state.get("gui_signal_artifacts", {})),
                                     ("review_attempt_failures", state.get("review_attempt_failures", []), state.get("review_attempt_failure_artifacts", {})),
                                     ("escalations", state.get("escalations", []), state.get("escalation_artifacts", {})),
                                     ("executor_recoveries", state.get("executor_recoveries", []), state.get("executor_recovery_artifacts", {})),
                                     ("cycle_triage", state.get("cycle_triage", []), state.get("cycle_triage_artifacts", {}))):
        for item in collection:
            artifact = _safe_file(root, f".codex-sync/tasks/{task_id}/implementation-review/{kind}/{item['id']}.json")
            raw = artifact.read_bytes()
            if _sha(raw) != hashes.get(item["id"]):
                raise ReviewError(f"immutable {kind[:-1]} artifact tampered")
            try:
                persisted = json.loads(raw.decode("utf-8"))
            except (ValueError, UnicodeError) as exc:
                raise ReviewError(f"invalid immutable {kind[:-1]} artifact") from exc
            if persisted != item:
                raise ReviewError(f"mutable {kind[:-1]} projection differs from immutable artifact")
        if set(hashes) != {item.get("id") for item in collection}:
            raise ReviewError(f"{kind} projection and immutable artifact index differ")
        artifact_dir = root / ".codex-sync" / "tasks" / task_id / "implementation-review" / kind
        actual_ids = {p.stem for p in artifact_dir.glob("*.json")} if artifact_dir.exists() else set()
        if actual_ids != set(hashes):
            raise ReviewError(f"{kind} immutable event files are missing, reordered, or unindexed")
    # Every review must consume exactly one persisted attempt, and the cycle
    # sequence must alternate review -> correction -> review. This makes the
    # artifact chain authoritative rather than trusting editable list order.
    if len(state["reviews"]) > len(state["review_attempts"]):
        raise ReviewError("review verdict has no persisted attempt")
    attempts = {a["id"]: a for a in state["review_attempts"]}
    for review in state["reviews"]:
        attempt = attempts.get(review["id"])
        if attempt is None or attempt.get("result_sha256") != review.get("result_sha256") or attempt.get("changed_files") != review.get("changed_files"):
            raise ReviewError("review verdict does not match its immutable attempt")
    correction_sources = [c.get("source_review") for c in state["corrections"]]
    if len(correction_sources) != len(set(correction_sources)):
        raise ReviewError("a review correction package was consumed more than once")
    for correction in state["corrections"]:
        source = next((r for r in state["reviews"] if r["id"] == correction.get("source_review")), None)
        if source is None or source.get("verdict") != "CHANGES REQUIRED" or correction.get("source_review_sha256") != state["review_artifacts"].get(source["id"]):
            raise ReviewError("correction is not bound to an actionable immutable review")
    for index, review in enumerate(state["reviews"][:-1]):
        if review["verdict"] != "CHANGES REQUIRED":
            raise ReviewError("event follows a terminal review verdict")
        correction = state["corrections"][index] if index < len(state["corrections"]) else None
        if correction is None or correction.get("source_review") != review["id"]:
            raise ReviewError("review/correction event order is incomplete")
    if len(state["corrections"]) > len(state["reviews"]):
        raise ReviewError("correction event follows current unresolved review")
    authorizations = state.get("correction_authorizations", [])
    authorization_ids = [item.get("id") for item in authorizations]
    if len(authorization_ids) != len(set(authorization_ids)):
        raise ReviewError("correction authorization event is duplicated")
    expected_pending = set(authorization_ids) - {item.get("id") for item in state["corrections"]}
    if set(state.get("pending_corrections", {})) != expected_pending:
        raise ReviewError("pending correction authorization is not derived from current events")
    auth_by_id = {item.get("id"): item for item in authorizations}
    for auth_id in expected_pending:
        auth = state["pending_corrections"][auth_id]
        if auth != auth_by_id.get(auth_id):
            raise ReviewError("pending correction authorization differs from its immutable event")
    for auth in authorizations:
        source = next((item for item in state["reviews"] if item.get("id") == auth.get("source_review")), None)
        if (source is None or source.get("verdict") != "CHANGES REQUIRED"
                or auth.get("source_review_sha256") != state["review_artifacts"].get(source["id"])
                or auth.get("id") not in state.get("correction_authorization_artifacts", {})):
            raise ReviewError("correction authorization is not bound to its actionable review event")
    recoveries = state.get("executor_recoveries", [])
    executor_identity = initial.get("identity")
    if state["executor"].get("initial_identity") != executor_identity:
        raise ReviewError("initial executor identity differs from immutable authority")
    for index, recovery in enumerate(recoveries, 1):
        if (recovery.get("id") != f"REC-{index}" or recovery.get("actor") != "GUI"
                or recovery.get("continuity_break") is not True
                or recovery.get("old_executor_identity") != executor_identity
                or recovery.get("correction_id") not in state.get("correction_authorization_artifacts", {})):
            raise ReviewError("executor recovery event is missing, reordered or fabricated")
        executor_identity = recovery.get("new_executor_identity")
    if executor_identity != state["executor"].get("identity"):
        raise ReviewError("executor identity differs from the latest continuity recovery event")
    if state["executor"].get("initial_actual_profile") != initial.get("actual_profile"):
        raise ReviewError("initial executor profile differs from immutable authority")
    return root, path, state


def _has_current_escalation(state, review_id):
    return any(item.get("source_review") == review_id
               and state.get("escalation_artifacts", {}).get(item.get("id"))
               for item in state.get("escalations", []))


def _validate_dispositions(previous, dispositions, *, allow_blocked=False):
    required = {f["id"] for f in previous["findings"]}
    if not isinstance(dispositions, dict) or set(dispositions) != required:
        raise ReviewError("every finding needs exactly one disposition")
    for key, value in dispositions.items():
        if (not isinstance(value, dict) or set(value) != {"disposition", "evidence"}
                or value["disposition"] not in DISPOSITIONS
                or not isinstance(value["evidence"], str)
                or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/# -]{0,159}", value["evidence"])
                or re.search(r"(?i)(/Users/|/home/|/private/|session[_ -]?(?:id|key)?\s*[:=])", value["evidence"])):
            raise ReviewError(f"finding {key} needs a valid evidenced disposition")
        if not allow_blocked and value["disposition"] in {"CANNOT FIX WITHIN SCOPE", "BLOCKED"}:
            raise ReviewError("blocked/out-of-scope finding requires GUI escalation, not a correction")


def authorize_correction(root, task_id: str, *, correction_id: str, source_review: str,
                         dispositions: dict, executor_identity: str | None):
    """Consume one package before edits, archive the completed handoff, and reopen it."""
    with _paired_lifecycle_lock(root, task_id):
        root, lifecycle_path, state = _load(root, task_id)
        if not state["contract"]["loop"]["enabled"]: raise ReviewError("review loop is disabled")
        if correction_id in state.get("correction_authorization_artifacts", {}):
            auth = state["pending_corrections"].get(correction_id)
            if not auth or auth.get("source_review") != source_review or auth.get("dispositions") != dispositions:
                raise ReviewError("correction authorization replay conflicts with frozen package")
            _reopen_bound_handoff(root, state, auth)
            return auth
        previous = state["reviews"][-1] if state["reviews"] else None
        if previous is None or previous["id"] != source_review or previous["verdict"] != "CHANGES REQUIRED":
            raise ReviewError("correction package is stale or not actionable")
        if _has_current_escalation(state, source_review): raise ReviewError("current review is already escalated to GUI")
        if any(c.get("source_review") == source_review for c in state["corrections"]):
            raise ReviewError("correction package has already been consumed")
        if any(c.get("source_review") == source_review for c in state.get("pending_corrections", {}).values()):
            raise ReviewError("correction package already has a pending authorization")
        loop = state["contract"]["loop"]
        if (loop.get("correction_policy", "MAX_CYCLES") == "MAX_CYCLES"
                and len(state["corrections"]) + len(state.get("pending_corrections", {})) >= loop["correction_budget"]):
            raise ReviewError("selected correction budget is exhausted; escalate to GUI")
        _validate_dispositions(previous, dispositions)
        if state["executor"].get("identity") is not None and executor_identity != state["executor"].get("identity"):
            raise ReviewError("correction must remain in the original executor session")
        binding = state["handoff_binding"]
        status = _load_payload(root, f".codex-sync/tasks/{task_id}/STATUS.json")
        if status.get("status") != "COMPLETED" or status.get("result_sha256") != state["result_sha256"]:
            raise ReviewError("correction authorization requires the current completed result")
        auth = {"id": correction_id, "source_review": source_review,
                "source_review_sha256": state["review_artifacts"][source_review],
                "previous_result_sha256": state["result_sha256"],
                "previous_changed_files": state["changed_files"], "dispositions": dispositions,
                "executor_identity": executor_identity, "owner": binding.get("owner"),
                "handoff_revision": status["revision"],
                "created_at": datetime.now(timezone.utc).isoformat()}
        artifact_hash = _sha(_canonical(auth) + b"\n")
        state.setdefault("pending_corrections", {})[correction_id] = auth
        state.setdefault("correction_authorizations", []).append(auth)
        state.setdefault("correction_authorization_artifacts", {})[correction_id] = artifact_hash
        _commit_transition(root, task_id, state, [("correction_authorizations", auth)])
        _reopen_bound_handoff(root, state, auth)
        return auth


def escalate_correction(root, task_id: str, *, source_review: str, dispositions: dict, reason: str):
    """Return a blocked/out-of-scope correction decision to GUI with evidence."""
    if not isinstance(reason, str) or not reason.strip() or len(reason) > 1000:
        raise ReviewError("escalation requires a concise reason")
    with _paired_lifecycle_lock(root, task_id):
        root, path, state = _load(root, task_id)
        previous = state["reviews"][-1] if state["reviews"] else None
        if previous is None or previous["id"] != source_review or previous["verdict"] != "CHANGES REQUIRED":
            raise ReviewError("escalation package is stale or not actionable")
        if source_review in {e.get("source_review") for e in state.get("escalations", [])}:
            raise ReviewError("this review already has an escalation disposition")
        _validate_dispositions(previous, dispositions, allow_blocked=True)
        if not any(d["disposition"] in {"CANNOT FIX WITHIN SCOPE", "BLOCKED"} for d in dispositions.values()):
            raise ReviewError("correction escalation requires a blocked or out-of-scope finding")
        record = {"id": f"ESC-{len(state.get('escalations', [])) + 1}", "source_review": source_review,
                  "source_review_sha256": state["review_artifacts"][source_review],
                  "reason": reason.strip(), "dispositions": dispositions,
                  "carried_findings": previous["findings"],
                  "created_at": datetime.now(timezone.utc).isoformat()}
        artifact_hash = _sha(_canonical(record) + b"\n")
        state.setdefault("escalations", []).append(record)
        state.setdefault("escalation_artifacts", {})[record["id"]] = artifact_hash
        state["escalation"] = reason.strip()
        state["ready_for_gui"] = True
        _commit_transition(root, task_id, state, [("escalations", record)])
        _write_final_receipt(root, task_id, state)
        return record


def authorize_executor_recovery(root, task_id: str, *, correction_id: str,
                               new_executor_identity: str, reason: str, actor: str):
    """Record a GUI-approved continuity break for a lost original executor session."""
    if actor != "GUI": raise ReviewError("executor continuity recovery is GUI-owned")
    if not isinstance(new_executor_identity, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}", new_executor_identity):
        raise ReviewError("recovery requires a bounded replacement executor identity")
    if not isinstance(reason, str) or not reason.strip() or len(reason) > 1000:
        raise ReviewError("recovery requires the GUI's continuity-break reason")
    with _paired_lifecycle_lock(root, task_id):
        root, path, state = _load(root, task_id)
        auth = state.get("pending_corrections", {}).get(correction_id)
        status = _load_payload(root, f".codex-sync/tasks/{task_id}/STATUS.json")
        if (auth is None or status.get("status") != "IN_PROGRESS"
                or status.get("implementation_review_correction_id") != correction_id):
            raise ReviewError("executor recovery requires the current authorized in-progress correction")
        old_identity = state["executor"].get("identity")
        if old_identity is None or old_identity == new_executor_identity:
            raise ReviewError("continuity break requires a known lost identity and a distinct replacement")
        recovery_id = f"REC-{len(state.get('executor_recoveries', [])) + 1}"
        record = {"id": recovery_id, "correction_id": correction_id,
                  "source_review": auth["source_review"], "old_executor_identity": old_identity,
                  "new_executor_identity": new_executor_identity,
                  "handoff_revision": status["revision"], "reason": reason.strip(),
                  "continuity_break": True, "actor": actor,
                  "created_at": datetime.now(timezone.utc).isoformat()}
        artifact_hash = _sha(_canonical(record) + b"\n")
        state.setdefault("executor_recoveries", []).append(record)
        state.setdefault("executor_recovery_artifacts", {})[recovery_id] = artifact_hash
        state["executor"]["identity"] = new_executor_identity
        _commit_transition(root, task_id, state, [("executor_recoveries", record)])
        _write_final_receipt(root, task_id, state)
        return record


def _known_executor_identities(state):
    """Identities from the immutable initial snapshot and validated recovery chain."""
    identities = set()
    initial = state.get("executor_initial", {}).get("identity")
    if initial is not None: identities.add(initial)
    for recovery in state.get("executor_recoveries", []):
        for key in ("old_executor_identity", "new_executor_identity"):
            if recovery.get(key) is not None: identities.add(recovery[key])
    return identities


def _reopen_bound_handoff(root, state, auth):
    module_path = Path(__file__).resolve().with_name("handoff.py")
    spec = importlib.util.spec_from_file_location("handoff_correction_bridge", module_path)
    if spec is None or spec.loader is None: raise ReviewError("handoff lifecycle helper cannot be loaded")
    helper = importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
    try:
        helper.reopen_for_implementation_correction(root, state["task_id"],
            expected_revision=auth["handoff_revision"], correction_id=auth["id"],
            review_id=auth["source_review"], review_sha256=auth["source_review_sha256"],
            prior_result_sha256=auth["previous_result_sha256"],
            prior_changed_files=auth["previous_changed_files"], lock_held=True)
    except (ValueError, OSError) as exc:
        raise ReviewError(f"existing handoff correction transition failed: {exc}") from exc


def begin_review(root, task_id: str, *, review_id: str, result_path: str, changed_paths: list[str],
                 reviewer_identity: str | None = None):
    """Persist a bounded fresh-review attempt before reviewer analysis begins."""
    _validate_identity(reviewer_identity, "reviewer")
    with _paired_lifecycle_lock(root, task_id):
        root, lifecycle_path, state = _load(root, task_id)
        _, handoff_current = _verify_handoff_binding(root, state)
        if not handoff_current:
            raise ReviewError("fresh review requires the corrected result to pass normal handoff completion")
        if not state["contract"]["loop"]["enabled"]: raise ReviewError("review loop is disabled")
        if review_id in state["review_attempt_artifacts"]: raise ReviewError("review attempt ID replay")
        closed_attempts = {r["id"] for r in state["reviews"]} | {f["review_id"] for f in state.get("review_attempt_failures", [])}
        if any(a["id"] not in closed_attempts for a in state["review_attempts"]):
            raise ReviewError("prior review attempt must produce a verdict or explicit failure record")
        if state["reviews"] and state["reviews"][-1]["verdict"] != "CHANGES REQUIRED":
            raise ReviewError("review lifecycle already has a terminal verdict")
        if state["reviews"] and _has_current_escalation(state, state["reviews"][-1]["id"]):
            raise ReviewError("review lifecycle already has a current GUI escalation")
        if state["reviews"]:
            latest = state["reviews"][-1]
            if latest["verdict"] == "CHANGES REQUIRED":
                correction = next((c for c in state["corrections"] if c.get("source_review") == latest["id"]), None)
                handoff_status = _load_payload(root, f".codex-sync/tasks/{task_id}/STATUS.json")
                if correction is None or handoff_status.get("status") not in {"COMPLETED", "CONSUMED"} \
                        or handoff_status.get("result_sha256") != state.get("result_sha256"):
                    raise ReviewError("fresh review requires a consumed correction and completed current corrected result")
        if reviewer_identity and (reviewer_identity in _known_executor_identities(state) or
                                  any(r.get("reviewer_identity") == reviewer_identity for r in state["reviews"]) or
                                  any(a.get("reviewer_identity") == reviewer_identity for a in state["review_attempts"])):
            raise ReviewError("reviewer identity is not independent")
        if state["executor"].get("identity") is not None and reviewer_identity is None:
            raise ReviewError("known executor identity cannot be bypassed by omitting reviewer identity")
        result = _safe_file(root, result_path)
        result_hash = _sha(result.read_bytes()); files = {}
        for rel in sorted(set(changed_paths)):
            files[rel] = _sha(_safe_file(root, rel).read_bytes())
        if result_hash != state["result_sha256"] or files != state["changed_files"]:
            raise ReviewError("review attempt does not bind the current completed result")
        record = {"id": review_id, "task_id": task_id, "contract_sha256": state["contract_sha256"],
                  "result_sha256": result_hash, "changed_files": files, "reviewer_identity": reviewer_identity,
                  "requested_profile": state["contract"]["review"]["profile"],
                  "created_at": datetime.now(timezone.utc).isoformat()}
        artifact_hash = _sha(_canonical(record) + b"\n")
        state["review_attempts"].append(record); state["review_attempt_artifacts"][review_id] = artifact_hash
        _commit_transition(root, task_id, state, [("review_attempts", record)])
        return record


def fail_review_attempt(root, task_id: str, *, review_id: str, reason: str):
    """Preserve a failed/interrupted reviewer attempt without a verdict."""
    if not isinstance(reason, str) or not reason.strip(): raise ReviewError("attempt failure needs a reason")
    with _paired_lifecycle_lock(root, task_id):
        root, path, state = _load(root, task_id)
        attempt = next((a for a in state["review_attempts"] if a["id"] == review_id), None)
        if attempt is None or any(r["id"] == review_id for r in state["reviews"]):
            raise ReviewError("review attempt is absent or already has a verdict")
        key = f"{review_id}-FAILURE"
        record = {"id": key, "review_id": review_id, "attempt_sha256": state["review_attempt_artifacts"][review_id],
                  "state": "FAILED_OR_INTERRUPTED", "reason": reason.strip(),
                  "created_at": datetime.now(timezone.utc).isoformat()}
        artifact_hash = _sha(_canonical(record) + b"\n")
        state.setdefault("review_attempt_failures", []).append(record)
        state.setdefault("review_attempt_failure_artifacts", {})[key] = artifact_hash
        _commit_transition(root, task_id, state, [("review_attempt_failures", record)])
        return record


def status(root, task_id, *, lock_held=False):
    """Return a deterministic status projection from persisted artifacts."""
    root = Path(root).resolve(strict=True)
    if lock_held:
        return _status_locked(root, task_id)
    with _paired_lifecycle_lock(root, task_id):
        return _status_locked(root, task_id)


def _status_locked(root, task_id):
    _, _, s = _load(root, task_id)
    latest = s["reviews"][-1] if s["reviews"] else None
    current_result = False
    try:
        result_path = _safe_file(Path(root).resolve(strict=True), s["result_path"])
        current_result = _sha(result_path.read_bytes()) == s["result_sha256"]
        for rel, expected in s["changed_files"].items():
            current_result = current_result and _sha(_safe_file(Path(root).resolve(strict=True), rel).read_bytes()) == expected
    except (OSError, ReviewError):
        current_result = False
    _, handoff_current = _verify_handoff_binding(Path(root).resolve(strict=True), s)
    current_terminal = bool(latest and latest["verdict"] in {"ACCEPTED", "ESCALATE TO GUI"}
                            and latest.get("result_sha256") == s["result_sha256"])
    event_escalation = bool(latest
                            and any(e.get("source_review") == latest["id"]
                                    and s["escalation_artifacts"].get(e.get("id"))
                                    for e in s["escalations"]))
    current_escalation = next((e.get("reason") for e in reversed(s["escalations"])
                               if latest and e.get("source_review") == latest["id"]
                               and s["escalation_artifacts"].get(e.get("id"))), None)
    ready = bool(current_result and handoff_current
                 and ((current_terminal and latest["verdict"] == "ACCEPTED") or event_escalation))
    if ready and any(signal.get("type") == "gui_acceptance_rejected" and signal.get("review_id") == latest["id"]
                     for signal in s.get("gui_signals", [])):
        ready = False
    count = len(s["corrections"])
    policy = s["contract"]["loop"].get("correction_policy", "MAX_CYCLES")
    limit = s["contract"]["loop"]["correction_budget"]
    return {"task_id": task_id, "executor": "COMPLETE" if s["result_sha256"] else "INCOMPLETE",
            "latest_review": None if latest is None else {"id": latest["id"], "verdict": latest["verdict"],
                                                           "findings": len(latest["findings"])},
            "correction_policy": policy, "review_count": len(s["reviews"]),
            "correction_count": count, "correction_limit": limit,
            "ready_for_gui": ready, "escalation": current_escalation}


def submit_review(root, task_id: str, *, review_id: str, verdict: str, findings: list,
                  result_path: str, changed_paths: list[str], reviewer_identity: str | None,
                  reviewer_profile: dict | None, dimensions: dict, read_only_attestation: bool,
                  telemetry: dict | None = None, resolutions: dict | None = None,
                  escalation_reason: str | None = None):
    """Append one fresh-review verdict; never writes implementation files."""
    with _paired_lifecycle_lock(root, task_id):
        return _submit_review_locked(root, task_id, review_id=review_id, verdict=verdict, findings=findings,
            result_path=result_path, changed_paths=changed_paths, reviewer_identity=reviewer_identity,
            reviewer_profile=reviewer_profile, dimensions=dimensions, read_only_attestation=read_only_attestation,
            telemetry=telemetry, resolutions=resolutions, escalation_reason=escalation_reason)


def _submit_review_locked(root, task_id: str, *, review_id: str, verdict: str, findings: list,
                  result_path: str, changed_paths: list[str], reviewer_identity: str | None,
                  reviewer_profile: dict | None, dimensions: dict, read_only_attestation: bool,
                  telemetry: dict | None = None, resolutions: dict | None = None,
                  escalation_reason: str | None = None):
    root, lifecycle_path, s = _load(root, task_id)
    _validate_identity(reviewer_identity, "reviewer")
    _validate_actual_profile(reviewer_profile, "reviewer")
    if not s["contract"]["loop"]["enabled"]: raise ReviewError("review loop is disabled")
    if s["executor"].get("identity") is not None and reviewer_identity is None:
        raise ReviewError("known executor identity cannot be bypassed by omitting reviewer identity")
    if verdict not in VERDICTS: raise ReviewError("invalid reviewer verdict")
    if verdict == "ESCALATE TO GUI" and (not isinstance(escalation_reason, str) or not escalation_reason.strip()):
        raise ReviewError("GUI escalation requires a persisted reason")
    if not read_only_attestation: raise ReviewError("reviewer must attest implementation was read-only")
    if reviewer_identity and (reviewer_identity in _known_executor_identities(s) or
                              any(r.get("reviewer_identity") == reviewer_identity for r in s["reviews"])):
        raise ReviewError("reviewer identity is not independent")
    if review_id in {r["id"] for r in s["reviews"]}: raise ReviewError("review ID replay")
    attempt = next((a for a in s["review_attempts"] if a["id"] == review_id), None)
    if attempt is None or any(f.get("review_id") == review_id for f in s.get("review_attempt_failures", [])):
        raise ReviewError("review requires an open persisted attempt")
    if attempt.get("reviewer_identity") != reviewer_identity:
        raise ReviewError("review identity differs from the identity frozen at attempt start")
    if set(dimensions) != set(REVIEW_DIMENSIONS) or any(not isinstance(x, str) or not x.strip() for x in dimensions.values()):
        raise ReviewError("every frozen review dimension needs a disposition/evidence note")
    result = _safe_file(root, result_path)
    result_hash = _sha(result.read_bytes())
    files = {}
    for rel in sorted(set(changed_paths)):
        p = _safe_file(root, rel); files[rel] = _sha(p.read_bytes())
    if result_hash != s["result_sha256"] or files != s["changed_files"]:
        raise ReviewError("stale result or changed-file bytes; create a new paired contract/revision")
    if attempt["result_sha256"] != result_hash or attempt["changed_files"] != files:
        raise ReviewError("review attempt no longer matches current result")
    if len(files) > s["contract"]["review"]["budget"]["max_changed_files"]:
        raise ReviewError("review exceeds frozen changed-file budget")
    if not isinstance(findings, list): raise ReviewError("findings must be a list")
    for finding in findings:
        if not isinstance(finding, dict) or set(finding) != {"id", "category", "severity", "criterion", "evidence", "problem", "correction_boundary", "status"}:
            raise ReviewError("finding fields must identify category, severity, criterion, evidence, problem, correction boundary and status")
        if not all(isinstance(finding[k], str) and finding[k].strip() for k in finding):
            raise ReviewError("finding fields must be nonempty strings")
        if (not re.fullmatch(r"[A-Z][A-Z0-9-]{0,39}", finding["id"])
                or finding["severity"].lower() not in {"critical", "high", "medium", "low"}
                or finding["status"] != "OPEN"):
            raise ReviewError("finding ID or severity is invalid")
    if verdict == "CHANGES REQUIRED" and not findings: raise ReviewError("CHANGES REQUIRED needs findings")
    if len(findings) > s["contract"]["review"]["budget"]["max_evidence_items"]:
        raise ReviewError("review exceeds frozen evidence-item budget")
    if verdict != "CHANGES REQUIRED" and findings: raise ReviewError("only CHANGES REQUIRED carries correction findings")
    if s["reviews"] and s["reviews"][-1]["verdict"] != "CHANGES REQUIRED":
        raise ReviewError("review lifecycle already has a terminal verdict")
    if s["reviews"] and _has_current_escalation(s, s["reviews"][-1]["id"]):
        raise ReviewError("review lifecycle already has a current GUI escalation")
    prior = s["reviews"][-1] if s["reviews"] else None
    expected_resolutions = set()
    outstanding_prior = set()
    correction = None
    if prior is not None:
        correction = next((c for c in s["corrections"] if c.get("source_review") == prior["id"]), None)
        if correction is None:
            raise ReviewError("prior findings have no consumed correction disposition")
        expected_resolutions = {f["id"] for f in prior["findings"]}
        if not isinstance(resolutions, dict) or set(resolutions) != expected_resolutions:
            raise ReviewError("fresh reviewer must resolve every prior finding explicitly")
        for finding_id, outcome in resolutions.items():
            if (not isinstance(outcome, dict) or set(outcome) != {"status", "evidence"}
                    or outcome["status"] not in {"RESOLVED", "NOT APPLICABLE", "UNRESOLVED", "REGRESSION"}
                    or not isinstance(outcome["evidence"], str) or not outcome["evidence"].strip()
                    or len(outcome["evidence"]) > 300):
                raise ReviewError(f"invalid reviewer resolution for {finding_id}")
            if outcome["status"] != "RESOLVED":
                outstanding_prior.add(finding_id)
        if any(outcome["status"] != "RESOLVED" for outcome in resolutions.values()) and verdict == "ACCEPTED":
            raise ReviewError("reviewer cannot accept unresolved or regressed findings")
    elif resolutions:
        raise ReviewError("first review cannot claim resolutions")
    if verdict == "CHANGES REQUIRED" and not outstanding_prior.issubset({f["id"] for f in findings}):
        raise ReviewError("CHANGES REQUIRED must carry every unresolved or regressed prior finding")
    escalated_findings = []
    auto_escalation = None
    policy = s["contract"]["loop"].get("correction_policy", "MAX_CYCLES")
    limit = s["contract"]["loop"]["correction_budget"]
    if verdict == "CHANGES REQUIRED" and policy == "MAX_CYCLES" and len(s["corrections"]) >= limit:
        auto_escalation = "selected correction budget exhausted after " + str(len(s["corrections"])) + " corrections"
    if auto_escalation:
        carried = {f["id"]: f for f in prior.get("findings", []) if f["id"] in outstanding_prior} if prior else {}
        carried.update({f["id"]: f for f in findings})
        verdict = "ESCALATE TO GUI"; escalated_findings = list(carried.values()); findings = []
        escalation_reason = auto_escalation
    elif verdict == "ESCALATE TO GUI" and prior:
        escalated_findings = [f for f in prior.get("findings", []) if f["id"] in outstanding_prior]
    review = {"id": review_id, "verdict": verdict, "findings": findings,
              "contract_sha256": s["contract_sha256"], "result_sha256": result_hash, "changed_files": files, "dimensions": dimensions,
              "reviewer_identity": reviewer_identity, "requested_profile": s["contract"]["review"]["profile"],
              "actual_profile": reviewer_profile, "telemetry": validate_cycle_telemetry(telemetry),
              "resolutions": resolutions or {},
              "escalation_reason": escalation_reason if verdict == "ESCALATE TO GUI" else None,
              "escalated_findings": escalated_findings,
              "created_at": datetime.now(timezone.utc).isoformat()}
    if verdict == "CHANGES REQUIRED":
        review["correction_command"] = f"popraw {task_id} {review_id}"
    artifact_hash = _sha(_canonical(review) + b"\n")
    transaction_artifacts = [("reviews", review)]
    s["reviews"].append(review)
    s["review_artifacts"][review_id] = artifact_hash
    if verdict == "ESCALATE TO GUI":
        reason = escalation_reason or "reviewer escalation"
        record = {"id": f"ESC-{len(s.get('escalations', [])) + 1}", "source_review": review_id,
                  "source_review_sha256": artifact_hash, "reason": reason,
                  "carried_findings": escalated_findings, "created_at": datetime.now(timezone.utc).isoformat()}
        esc_hash = _sha(_canonical(record) + b"\n")
        s.setdefault("escalations", []).append(record)
        s.setdefault("escalation_artifacts", {})[record["id"]] = esc_hash
        s["escalation"] = reason
        transaction_artifacts.append(("escalations", record))
    s["ready_for_gui"] = verdict in {"ACCEPTED", "ESCALATE TO GUI"}
    _commit_transition(root, task_id, s, transaction_artifacts)
    if verdict in {"ACCEPTED", "ESCALATE TO GUI"}:
        _write_final_receipt(root, task_id, s)
    return review


def correct(root, task_id: str, *, correction_id: str, source_review: str, dispositions: dict,
            new_result_path: str, changed_paths: list[str], executor_identity: str | None,
            telemetry: dict | None = None):
    """Bind one same-executor correction to a current CHANGES REQUIRED package."""
    with _paired_lifecycle_lock(root, task_id):
        return _correct_locked(root, task_id, correction_id=correction_id, source_review=source_review,
            dispositions=dispositions, new_result_path=new_result_path, changed_paths=changed_paths,
            executor_identity=executor_identity, telemetry=telemetry)


def _correct_locked(root, task_id: str, *, correction_id: str, source_review: str, dispositions: dict,
            new_result_path: str, changed_paths: list[str], executor_identity: str | None,
            telemetry: dict | None = None):
    root, lifecycle_path, s = _load(root, task_id)
    if not s["contract"]["loop"]["enabled"]: raise ReviewError("review loop is disabled")
    previous = s["reviews"][-1] if s["reviews"] else None
    if previous is None or previous["id"] != source_review or previous["verdict"] != "CHANGES REQUIRED":
        raise ReviewError("correction package is stale or not actionable")
    if _has_current_escalation(s, source_review): raise ReviewError("current review is already escalated to GUI")
    auth = s.get("pending_corrections", {}).get(correction_id)
    if auth is None or auth.get("source_review") != source_review:
        raise ReviewError("correction must be authorized before implementation edits")
    if any(c.get("source_review") == source_review for c in s["corrections"]):
        raise ReviewError("correction package has already been consumed")
    loop = s["contract"]["loop"]
    if (loop.get("correction_policy", "MAX_CYCLES") == "MAX_CYCLES"
            and len(s["corrections"]) >= loop["correction_budget"]):
        raise ReviewError("selected correction budget is exhausted; escalate to GUI")
    if s["review_artifacts"].get(source_review) is None:
        raise ReviewError("correction source review has no immutable artifact binding")
    if s["executor"].get("identity") is not None and executor_identity != s["executor"].get("identity"):
        raise ReviewError("correction must remain in the original executor session")
    if correction_id in {c["id"] for c in s["corrections"]}: raise ReviewError("correction replay")
    _validate_dispositions(previous, dispositions)
    if auth["dispositions"] != dispositions:
        raise ReviewError("correction disposition differs from the consumed package")
    handoff_status, current_binding = _verify_handoff_binding(root, s)
    if handoff_status.get("status") != "COMPLETED" or handoff_status.get("implementation_review_correction_id") != correction_id:
        raise ReviewError("corrected files must complete the existing handoff before review lifecycle finalization")
    result = _safe_file(root, new_result_path)
    files = {}
    for rel in sorted(set(changed_paths)):
        p = _safe_file(root, rel); files[rel] = _sha(p.read_bytes())
    if set(files) != set(s["changed_files"]):
        raise ReviewError("correction must preserve the frozen changed-file inventory")
    if new_result_path != f".codex-sync/tasks/{task_id}/CLI_RESULT.md":
        raise ReviewError("correction result must be the existing handoff CLI_RESULT.md")
    if handoff_status.get("result_sha256") != _sha(result.read_bytes()):
        raise ReviewError("corrected result does not match normal handoff completion")
    if any(handoff_status.get("outputs", {}).get(rel) != value for rel, value in files.items()):
        raise ReviewError("corrected output hashes do not match normal handoff completion")
    executor_report, executor_report_sha = _execution_review(root, new_result_path)
    record = {"id": correction_id, "source_review": source_review,
              "source_review_sha256": s["review_artifacts"][source_review],
              "previous_result_sha256": s["result_sha256"], "previous_changed_files": s["changed_files"],
              "dispositions": dispositions,
              "result_path": new_result_path, "result_sha256": _sha(result.read_bytes()),
              "changed_files": files, "executor_identity": executor_identity,
              "executor_report": executor_report, "executor_report_sha256": executor_report_sha,
              "telemetry": validate_cycle_telemetry(telemetry),
              "created_at": datetime.now(timezone.utc).isoformat()}
    artifact_hash = _sha(_canonical(record) + b"\n")
    s["corrections"].append(record); s["result_path"] = new_result_path
    s["pending_corrections"].pop(correction_id, None)
    s["correction_artifacts"][correction_id] = artifact_hash
    s["result_sha256"] = record["result_sha256"]; s["changed_files"] = files; s["ready_for_gui"] = False
    _commit_transition(root, task_id, s, [("corrections", record)])
    return record


def render_enabled_handoff(task_id: str, *, parent_id: str, contract: dict, time_steps: str, gui_estimate: str):
    """Render the established handoff rows and frozen plan last."""
    validate_contract(contract)
    _check_task_id(task_id)
    if contract["task_id"] != parent_id or task_id == parent_id:
        raise ReviewError("handoff renderer requires the registered delegation ID and its distinct frozen parent")
    execution, review = contract["execution"], contract["review"]
    executor = execution["executor_profile"]
    reviewer = review["profile"]
    executor_model = f'{executor["requested_model"]} / {executor["requested_reasoning"].title()}'
    reviewer_model = f'{reviewer["requested_model"]} / {reviewer["requested_reasoning"].title()}'
    loop = contract["loop"]
    policy = loop.get("correction_policy", "MAX_CYCLES")
    correction_text = (f"max {loop['correction_budget']} corrections" if policy == "MAX_CYCLES"
                       else "until accepted or escalated · no numeric correction limit")
    plan_bullets = execution["plan_of_execution"]
    if len(plan_bullets) > 10 or not plan_bullets: raise ReviewError("plan requires 1–10 bullets")
    routing = contract.get("routing")
    review_enabled = contract["loop"]["enabled"]
    if review_enabled:
        gui_return = f"gotowe {task_id} · after ACCEPTED or explicit escalation"
    elif routing and routing["execution_class"] == "DIAGNOSTIC":
        gui_return = f"gotowe {task_id} · after the existing diagnostic route"
    else:
        gui_return = f"gotowe {task_id} · after required checks; no independent review"
    rows = [("Executor / pickup", f"wykonaj {task_id}"),
            ("Executor model", f"{executor_model} · persistent session; reused for corrections"),
            ("Independent review", f"sprawdź {task_id}" if review_enabled else "none · existing diagnostic route only if escalated"),
            ("Reviewer model", f"{reviewer_model} · fresh session for every review" if review_enabled else "none"),
            ("Correction command", f"popraw {task_id} R<n> · original persistent executor session" if review_enabled else "none"),
            ("GUI return", gui_return),
            ("Correction loop", f"{correction_text} · {loop['budget_rationale']} · ACCEPTED / CHANGES REQUIRED / ESCALATE TO GUI" if review_enabled else "disabled · no independent review"),]
    if routing:
        rows.append(("Routing", routing_summary(routing)))
    rows += [
            ("Estimated CLI time / steps", time_steps),
            ("szacowane tokeny/wiadomości", gui_estimate),
            ("Plan of execution", "<br>".join("• " + html.escape(x, quote=False).replace("|", "\\|") for x in plan_bullets))]
    cell = lambda value: html.escape(str(value), quote=False).replace("|", "\\|").replace("\n", " ").replace("\r", " ")
    rendered = []
    for label, value in rows:
        safe_value = value if label == "Plan of execution" else cell(value)
        rendered.append(f"| {cell(label)} | {safe_value} |")
    return "| | Command / value |\n|---|---|\n" + "\n".join(rendered)


def record_gui_rejection(root, task_id: str, *, reason: str):
    """Record GUI's explicit rejection of a reviewer ACCEPTED verdict."""
    if not isinstance(reason, str) or not reason.strip(): raise ReviewError("GUI rejection requires a reason")
    with _paired_lifecycle_lock(root, task_id):
        return _record_gui_rejection_locked(root, task_id, reason=reason)


def _record_gui_rejection_locked(root, task_id: str, *, reason: str):
    root, path, state = _load(root, task_id)
    if not state["reviews"] or state["reviews"][-1]["verdict"] != "ACCEPTED":
        raise ReviewError("GUI can reject only the current ACCEPTED result")
    signal_id = f"GUI-REJECT-{len(state.get('gui_signals', [])) + 1}"
    signal = {"id": signal_id, "type": "gui_acceptance_rejected", "reason": reason.strip(),
              "review_id": state["reviews"][-1]["id"], "created_at": datetime.now(timezone.utc).isoformat()}
    artifact_hash = _sha(_canonical(signal) + b"\n")
    state.setdefault("gui_signals", []).append(signal); state["ready_for_gui"] = False
    state.setdefault("gui_signal_artifacts", {})[signal_id] = artifact_hash
    _commit_transition(root, task_id, state, [("gui_signals", signal)])
    _write_final_receipt(root, task_id, state)
    return signal


def _load_payload(root: Path, rel: str):
    path = _safe_file(root, rel)
    try: return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, UnicodeError) as exc: raise ReviewError("invalid JSON payload") from exc


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    commands = parser.add_subparsers(dest="command", required=True)
    p = commands.add_parser("status"); p.add_argument("task_id")
    p = commands.add_parser("recover-transition"); p.add_argument("task_id")
    p = commands.add_parser("cycles"); p.add_argument("task_id")
    p = commands.add_parser("receipt"); p.add_argument("task_id")
    p = commands.add_parser("record-cycle-triage"); p.add_argument("task_id"); p.add_argument("cycle_id"); p.add_argument("inventory"); p.add_argument("--actor", required=True)
    p = commands.add_parser("initialize"); p.add_argument("task_id"); p.add_argument("contract_json"); p.add_argument("result_path"); p.add_argument("--changed", action="append", default=[]); p.add_argument("--executor-identity"); p.add_argument("--executor-actual-model"); p.add_argument("--executor-actual-reasoning")
    p = commands.add_parser("begin-review"); p.add_argument("task_id"); p.add_argument("review_id"); p.add_argument("result_path"); p.add_argument("--changed", action="append", default=[]); p.add_argument("--reviewer-identity")
    p = commands.add_parser("fail-review"); p.add_argument("task_id"); p.add_argument("review_id"); p.add_argument("--reason", required=True)
    p = commands.add_parser("review"); p.add_argument("task_id"); p.add_argument("review_json")
    p = commands.add_parser("authorize-correction"); p.add_argument("task_id"); p.add_argument("correction_json")
    p = commands.add_parser("escalate-correction"); p.add_argument("task_id"); p.add_argument("correction_json")
    p = commands.add_parser("authorize-executor-recovery"); p.add_argument("task_id"); p.add_argument("correction_id"); p.add_argument("new_executor_identity"); p.add_argument("--reason", required=True); p.add_argument("--actor", required=True)
    p = commands.add_parser("correct"); p.add_argument("task_id"); p.add_argument("correction_json")
    p = commands.add_parser("gui-reject"); p.add_argument("task_id"); p.add_argument("--reason", required=True)
    args = parser.parse_args(argv); root = Path(args.root).resolve(strict=True)
    try:
        if args.command == "status": value = status(root, args.task_id)
        elif args.command == "recover-transition": value = recover_transition(root, args.task_id)
        elif args.command == "cycles": value = cycle_reports(root, args.task_id)
        elif args.command == "receipt":
            require_final_receipt(root, args.task_id)
            value = render_final_receipt(root, args.task_id)
        elif args.command == "record-cycle-triage": value = record_cycle_triage(root, args.task_id, cycle_id=args.cycle_id, inventory_path=args.inventory, actor=args.actor)
        elif args.command == "initialize":
            contract_value = (_load_payload(root, args.contract_json[1:]) if args.contract_json.startswith("@")
                              else json.loads(args.contract_json))
            if bool(args.executor_actual_model) != bool(args.executor_actual_reasoning):
                raise ReviewError("actual executor model and reasoning must be supplied together")
            actual = ({"model": args.executor_actual_model, "reasoning": args.executor_actual_reasoning}
                      if args.executor_actual_model else None)
            value = initialize(root, args.task_id, contract_value, result_path=args.result_path, changed_paths=args.changed,
                               executor_identity=args.executor_identity, executor_actual_profile=actual)
        elif args.command == "begin-review": value = begin_review(root, args.task_id, review_id=args.review_id, result_path=args.result_path, changed_paths=args.changed, reviewer_identity=args.reviewer_identity)
        elif args.command == "fail-review": value = fail_review_attempt(root, args.task_id, review_id=args.review_id, reason=args.reason)
        elif args.command == "review":
            p = _load_payload(root, args.review_json)
            value = submit_review(root, args.task_id, review_id=p["review_id"], verdict=p["verdict"], findings=p["findings"], result_path=p["result_path"], changed_paths=p["changed_paths"], reviewer_identity=p.get("reviewer_identity"), reviewer_profile=p.get("actual_profile"), dimensions=p["dimensions"], read_only_attestation=p["read_only_attestation"], telemetry=p.get("telemetry"), resolutions=p.get("resolutions"), escalation_reason=p.get("escalation_reason"))
        elif args.command == "authorize-correction":
            p = _load_payload(root, args.correction_json)
            value = authorize_correction(root, args.task_id, correction_id=p["correction_id"], source_review=p["source_review"], dispositions=p["dispositions"], executor_identity=p.get("executor_identity"))
        elif args.command == "escalate-correction":
            p = _load_payload(root, args.correction_json)
            value = escalate_correction(root, args.task_id, source_review=p["source_review"], dispositions=p["dispositions"], reason=p["reason"])
        elif args.command == "authorize-executor-recovery":
            value = authorize_executor_recovery(root, args.task_id, correction_id=args.correction_id,
                new_executor_identity=args.new_executor_identity, reason=args.reason, actor=args.actor)
        elif args.command == "correct":
            p = _load_payload(root, args.correction_json)
            value = correct(root, args.task_id, correction_id=p["correction_id"], source_review=p["source_review"], dispositions=p["dispositions"], new_result_path=p["result_path"], changed_paths=p["changed_paths"], executor_identity=p.get("executor_identity"), telemetry=p.get("telemetry"))
        else: value = record_gui_rejection(root, args.task_id, reason=args.reason)
    except (ReviewError, ValueError, KeyError, OSError) as exc:
        print(f"implementation_review: {exc}", file=sys.stderr); return 2
    print(json.dumps(value if args.command != "status" else value, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__": raise SystemExit(main())
