# R-005 batched GUI lifecycle diagnostic

Historical A–E procedure for 1.20.1.1; not a pending test request.
Corrected C–D passed; first C had not entered global observer. A was not
explicitly reported; E retained ARMED and lacks a separate post-load R5 in
that capture. See README.md/current research summary before interpreting results.

Original hypothesis: ARM sets a
GUI VariableSystem marker; CLEAR means it is absent. A zero-size additive
startup widget clears it on _hide when GetPlayer.IsValid becomes false.
No visible overlay, map effects, gameplay state, save edits or world scans.

After startup approval, use a paused disposable game. Record actual statuses;
do not correct unexpected outcomes. R5 scope logs and character-change hook
remain installed. Do not overwrite a valued save.

| Step | Action | Record |
|---|---|---|
| A | Open +, press ARM; close/reopen + twice | Status after each reopening; expected ARMED |
| B | Switch directly to another dynastic ruler; reopen +, click R5 once | Old/new ruler, status; expected ARMED if validity never dropped, actual may differ |
| C | Press ARM again; close +; enter global observer; open + | Status; expected CLEAR, R5/R5N/ARM hidden |
| D | Return to a ruler; open +, click R5 once | Ruler/status; expected CLEAR and controls restored |
| E | Press ARM, click R5; save to a new R005-batch slot; reload; reopen + and click R5 | Ruler/status after load; marker persistence/reset is unknown |

Report A–E together, especially any unexpected state. Menu must be closed
before observer entry in C so the watcher is tested independently of the menu.
Stop on a crash or inaccessible interface. No succession/death manipulation
in this batch. No-Dynasty player UI and direct-invalid Execute remain open.

A successful CLEAR is GUI notification evidence only, not restoration of
barony colors or proof of robust production lifecycle behavior. Same-validity
player/Dynasty changes still need explicit revalidation and hook coverage.
