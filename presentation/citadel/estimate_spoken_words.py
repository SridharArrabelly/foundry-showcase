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
    if number > 17:
        continue
    body = section[2]
    clock = re.search(r"\*\*Clock (\d+):(\d+)–(\d+):(\d+)([^\n]*)", body)
    assert clock, f"No clock for slide {number}"
    start = int(clock[1]) + int(clock[2]) / 60
    end = int(clock[3]) + int(clock[4]) / 60
    transition = re.search(r"(\d+) (minute|second)s? transitions?", clock[5])
    transition_minutes = (
        int(transition[1]) / (60 if transition[2] == "second" else 1) if transition else 0
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
assert len(rows) == 17
assert sum(row["allocated_minutes"] for row in rows) == 80
total = sum(row["spoken_words"] for row in rows)
transitions = sum(row["booked_transition_minutes"] for row in rows)
result = {
    "method": "Count leading-curly-quote main-route paragraphs on visible slides 1–17, before each If branch; exclude stage directions, fenced/inline code, headings, backups, Q&A and appendices.",
    "tokenization": "Unicode word tokens; hyphenated/slashed terms count as one. Verbal expansion of numbers/IDs and unscripted commentary can add time.",
    "manuscript_sha256": hashlib.sha256(source.encode()).hexdigest(),
    "spoken_words": total, "content_budget_minutes": 80, "qa_budget_excluded_minutes": 10,
    "booked_transitions_minutes": transitions,
    "speech_minutes_by_words_per_minute": {str(rate): round(total / rate, 2) for rate in [120, 130, 140]},
    "remaining_for_non_narrated_demo_and_wait_minutes": {
        str(rate): round(80 - transitions - total / rate, 2) for rate in [120, 130, 140]
    },
    "first_six_slides_speech_plus_one_transition_minute_at_130wpm": round(
        sum(row["spoken_words"] for row in rows[:6]) / 130 + 1, 2
    ),
    "warnings": [
        "Do not add all 52 demo minutes as silent time: part of this script is spoken during demonstrations.",
        "Cover and architecture/transition slots are locally tight; the first 13-minute block has almost no spare time at 130 wpm.",
        "Slide 16 has only two minutes for a fresh call, inspection and close; preserve the 30-second fallback cutoff.",
        "A live four-session Memory run can add unscripted waits; the main route can use the verified redacted prior proof.",
        "This estimate is not a full human 90-minute rehearsal or a latency guarantee.",
    ],
    "human_90minute_rehearsal_performed": False,
    "slides": rows,
}
(ROOT / "spoken-word-estimate.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
print(json.dumps({key: value for key, value in result.items() if key != "slides"}, indent=2))
