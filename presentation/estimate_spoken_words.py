"""Reproducible main-route word estimate, not a human timing rehearsal."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).parent
source = (ROOT / "Presenter manuscript.md").read_text(encoding="utf-8")
rows = []
for section in re.finditer(
    r"(?ms)^## Slide (\d{2})[^\n]*\n(.*?)(?=^## Slide \d{2}|^## Appendix|\Z)", source
):
    number = int(section[1])
    if number > 23:
        continue
    body = section[2]
    clock = re.search(r"\*\*Clock (\d+):(\d+)–(\d+):(\d+)([^\n]*)", body)
    assert clock, f"No clock for slide {number}"
    start = int(clock[1]) + int(clock[2]) / 60
    end = int(clock[3]) + int(clock[4]) / 60
    transition = re.search(r"(?:(\d+) minutes?\s*)?(?:(\d+) seconds?\s*)?transitions?", clock[5])
    transition_minutes = (
        int(transition[1] or 0) + int(transition[2] or 0) / 60 if transition else 0
    )
    primary = body.split("**If ", 1)[0]
    primary = re.sub(r"(?ms)^```.*?^```\s*$", "", primary)
    spoken = [
        p.strip() for p in re.split(r"\n\s*\n", primary) if p.lstrip().startswith("“")
    ]
    words = "\n".join(spoken)
    words = re.sub(r"`[^`]*`|\[[^\]]*\]", "", words)
    count = len(re.findall(r"\b[\w]+(?:[’'/-][\w]+)*\b", words))
    minimum = count / 130 + transition_minutes
    rows.append({
        "slide": number, "spoken_words": count, "spoken_paragraphs": len(spoken),
        "allocated_minutes": round(end - start, 2),
        "booked_transition_minutes": transition_minutes,
        "speech_plus_transition_at_130wpm_minutes": round(minimum, 2),
        "excess_before_silent_demo_at_130wpm_seconds": round(max(0, minimum - (end - start)) * 60, 1),
    })
assert len(rows) == 23
assert sum(row["allocated_minutes"] for row in rows) == 80
total = sum(row["spoken_words"] for row in rows)
transitions = sum(row["booked_transition_minutes"] for row in rows)
result = {
    "method": "Count explicitly quoted talk-track paragraphs on content slides 1–23. This is a lower bound: imported source notes also contain unquoted guidance, not a complete verbatim speech. Exclude commands, cues, Q&A and hidden backups.",
    "tokenization": "Unicode word tokens; hyphenated/slashed terms count as one. Verbal expansion of numbers/IDs and unscripted commentary can add time.",
    "manuscript_sha256": hashlib.sha256(source.encode()).hexdigest(),
    "spoken_words": total, "content_budget_minutes": 80, "qa_budget_excluded_minutes": 10,
    "booked_transitions_minutes": transitions,
    "quoted_speech_lower_bound_minutes_by_words_per_minute": {str(rate): round(total / rate, 2) for rate in [120, 130, 140]},
    "remaining_demo_and_wait_minutes": None,
    "remaining_time_note": "Not inferred from partial speaker notes; rehearse the timed route.",
    "opening_six_slides_speech_minutes_at_130wpm": round(
        sum(row["spoken_words"] for row in rows[:6]) / 130, 2
    ),
    "warnings": [
        "Quoted talk-track only; do not treat these partial-note word counts as a complete speech duration.",
        "Demo-block narration overlaps interaction; do not count it twice as silent demonstration time.",
        "Leave deliberate time for case-level inspection and audience interpretation; don't fill every pause with narration.",
        "Preserve the 30-second fallback cutoff for fresh requests; finish Demo 4 at 70:00.",
        "The v2 cloud route is not activated; local tests and historical reports are explicitly distinct.",
        "This estimate is not a full human 90-minute rehearsal or a latency guarantee.",
    ],
    "human_90minute_rehearsal_performed": False,
    "slides": rows,
}
(ROOT / "spoken-word-estimate.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps({key: value for key, value in result.items() if key != "slides"}, indent=2))
