"""Prepare the adopted 26-slide source; never recreate the retired 24-slide deck."""

import argparse
from copy import deepcopy
from pathlib import Path
import re

from pptx import Presentation
from pptx.util import Pt

ROOT = Path(__file__).parent
OUTPUT = ROOT / "Can we defend this release - Foundry SE Showcase.pptx"
DEMOS = {8: (9, 21360), 13: (14, 10335), 16: (17, 13719), 20: (21, 24932)}
CLOCKS = [
    (0, 1), (1, 4), (4, 5), (5, 10), (10, 12), (12, 15), (15, 17), (17, 25),
    (25, 27), (27, 29), (29, 31), (31, 32), (32, 40), (40, 41), (41, 42),
    (42, 50), (50, 54), (54, 57), (57, 60), (60, 70), (70, 74), (74, 76),
    (76, 80), (80, 90),
]
REPLACEMENTS = {
    3: {15555: "90 minutes, one agent, two loops"},
    4: {16290: "Watch\nScheduled checks / Insights: planned"},
    7: {
        20008: "Recorded trace\n43 spans for one identified DEMO request",
        20205: "Distinct projects\nSeparate connections; shared account, not hard isolation",
        20508: "gpt-5.4-mini · Data Zone Standard. Sweden Central account location is not a Sweden-only processing guarantee.",
    },
    9: {
        21471: "BACK FROM DEMO 1 · PROVE",
        22881: "Fluent prose did not establish contract correctness.\nReal, unseeded defect: replacement-recall, DEV v1.",
    },
    10: {
        24300: "Historical prompt repair: DEV 9/9. New code boundary: locally tested, cloud deployment pending.\nTrade-off: buffered answer text and templated wording.",
    },
    11: {
        9237: "Does the prose invent an action? Eight calibration examples; cloud calibration pending.",
        9412: "Content-risk scan: adapter ready; SDK setup and actual scan pending.",
        9435: "Judge only what the completed checks establish. Local tests are not cloud scan results.",
    },
    12: {
        9624: "Recorded input marker: content_filter; ordinary requests separately exercised",
        9900: "no accepted improvement; Optimizer applied no candidate",
    },
    13: {
        10149: "1.  Historical baseline 8/9 and the failing row\n2.  Code, model and human evaluator roles\n3.  Local runtime and evaluator tests\n4.  Recorded guardrail; red-team scan pending\n5.  Optimizer: no accepted improvement",
        10287: "“Passing is bounded by the cases, rubric and attacks actually evaluated.”",
    },
    14: {
        10384: "BACK FROM DEMO 2 · BRIDGE 1",
        10434: "One gate for every behaviour change",
        10590: "Same-repository, non-draft PR",
        11112: "Native code grader + calibrated action rubric",
        11644: "Activation pending\nRequired status, reviewers and OIDC must be configured",
        11860: "Implemented, not activated · agent-pr-gate.yml + agent-release.yml · red teaming is a separate approved scan.",
    },
    15: {
        12240: "candidate/agent.zip  + SHA-256\ncandidate/deployment.json\ndev/native-evaluation.json\ndev/action-judgments.json  (includes calibration)\npromotion.json  (release artifact)\ndemo/summary.json  (release artifact)",
        12562: "What was checked?\nRubric verdicts; separate scan when available",
        12987: "Requested artifact retention: 90 days, subject to repository policy. Export approved evidence before expiry.",
    },
    16: {
        13345: "1.  Inspect the implemented workflow\n2.  Run local gate rejection checks\n3.  Open the historical release case file\n4.  Identify approvals and cloud proof still needed",
        13624: "“The case file explains what was tested. A future gate run is not evidence yet.”",
    },
    17: {
        13815: "BACK FROM DEMO 3 · OPERATE",
        14011: "After activation, capture or scoring failures open an issue for triage.",
        14111: "Prepared weekly check: pinned DEMO version, synthetic v1 cases. Not sampled live traffic or action-truthfulness scoring.",
        29653: "Prepared workflow; activation pending",
        30403: "Foundry agent Insights · not configured",
    },
    18: {14839: "Scored 1.0 on v1\nDecision, required tool and reference passed"},
    19: {
        24457: "Our recorded trace review surfaces it",
        24667: "Repeat the gate after approved activation",
    },
    20: {
        24814: "1.  Recorded claim and matching trace\n2.  Annotation and two new cases\n3.  Replay: v1 passes, v2 fails locally\n4.  Inspect the code repair and local tests\n5.  Cloud gate and scheduled checks: pending",
    },
    21: {
        24964: "BACK FROM DEMO 4 · ARCHITECTURE",
        31297: "Curated capability set; backend authorization still matters",
        31627: "Inspectable IQ; tool-supplied references",
        32335: "Implemented; cloud proof and approval controls pending",
        32617: "Tracing + planned scheduled checks",
        32713: "Observe requests; activate measurements deliberately",
    },
    25: {
        27252: "•  Customers, orders and policies are synthetic; 11 cases are not a readiness certificate.\n•  DEV and DEMO share an account, not a hard production isolation boundary.\n•  APIM Developer has no production SLA; account location is not processing residency.\n•  Copilot harness and Insights are previews.\n•  New cloud gate, red-team scan and weekly checks remain pending.\n•  Historical results do not prove the revised code is serving.",
    },
    26: {27642: "Historical DEV proof\nOne caller: remember, recall, forget and verified deletion. Revised UX awaits cloud validation."},
}
NOTES = {
    1: """“A useful agent is the beginning, not the release decision. Today we follow one synthetic Volt & Co customer through build, prove, release, operate and improve.

“We will distinguish historical cloud evidence from the revised local code. New cloud activation, calibration, red-team results and promotion are still pending. That distinction is how we defend a release rather than merely demonstrate one.”""",
    3: """“The agenda follows the lifecycle rather than the feature catalog. Four demonstrations answer four questions: how was the answer produced, what does passing establish, can we defend the artifact, and what did operation teach us?

“The two bridges connect developer work with operation. Keep Demo 1 at 17:00, Demo 2 at 32:00, Demo 3 at 42:00 and Demo 4 at 60:00. Protect the ten-minute Q&A.”""",
    7: """“Follow the customer request through the hosted agent, curated Toolbox and governed model/tool routes to the business and policy backends. Toolbox curation is not a substitute for backend authorization.

“The saved golden DEMO request has 43 correlated spans. Those spans identify that request, not today's invocation and not every future request. DEV and DEMO have distinct projects and connections but share an account.

“The APIM contracts cover configured application routes, not every internal evaluation, IQ or Memory call. They are not a universal spending cap. Now we will inspect the request and its evidence.”""",
    8: """“Let us inspect the golden replacement request and distinguish the model's tool choices from the business decision.

[SWITCH OUT: use docs/DEMO-RUNBOOK.md Demo 1 only after its cloud prerequisites are met. Until then, open Recorded evidence.html → Released DEMO v1 → replacement-recall and identify it as historical. Do not expect serving v1 to contain the new renderer.]

“Compare identifiers, actual calls, outputs and policy references. A catalog entry is configuration; a matched call and result is execution evidence.

[Show the saved response's matching trace, then the current local evidence_contract.py. A fresh request needs its own correlated trace. Stop waiting after 30 seconds; never borrow another run's identity.]""",
    9: """“The historical DEV baseline passed eight of nine cases. In the failing case the tool returned eligible while the response said recommendation. Fluent wording did not preserve the structured business meaning.

“The v1 grader checked the reviewed expected decision, required successful tool and reference. V2 additionally compares actual returned status and arguments. We retain independent expected outcomes so a broken tool and answer cannot pass simply by agreeing.”""",
    10: """“The historical repair changed instructions and achieved nine of nine. The newer application boundary is different: code derives the decision from this run's tool evidence and constrains the customer answer.

“The model still interprets the request, selects tools and extracts identifiers. The trade-off is templated wording and buffered customer text, not removal of the streaming protocol. The new code has local Agent and Responses-host proof; deployment remains pending.”""",
    11: """“Code checks exact expectations, arguments, outcomes and references. A model rubric checks the meaning of action claims. Human review supplies the expectation when language is ambiguous.

“Eight positive and negative calibration examples are authored, but they have not been calibrated in Azure. The red-team adapter is implemented; SDK installation and the actual content-risk scan remain pending. Neither is represented by a passing local unit test.

“The regression dataset retains the original nine expectations and adds two customer-language escalation cases. Eleven synthetic cases are a bounded regression suite.”""",
    12: """“The recorded guardrail marker produced a native content_filter block. Ordinary utility was exercised separately. That is specific evidence, not proof of every guardrail boundary.

“The completed Optimizer experiment retained its baseline at 0.75. No improved candidate was accepted or applied. That is different from the separate instructions-only business repair and promotion.

“A tool-boundary control remains a separately approved follow-up.”""",
    13: """[SWITCH OUT: inspect the recorded DEV baseline and failed row, then the v2 code grader and action rubric. Run the existing local runtime/evaluation command from the runbook.]

“Local tests show the actual Agent tool loop and Responses stream enforce the output boundary. They do not prove a new Azure deployment.

[Show the recorded guardrail result and completed Optimizer result. Red-team scorecard: unavailable until a genuine scan succeeds; explain the planned check rather than inventing a result.]""",
    14: """“This is the designed release mechanism, not a claim that the cloud gate is activated. Credential-free checks run now. Live jobs require the activation variable, real environment reviewers, scoped identities and the required branch status.

“After approval, the gate deploys and evaluates an exact candidate. The release consumes its ZIP, dataset and grader identities, without rebuilding. Red teaming is a separate scan, not silently included in the business gate.”""",
    15: """“The case file contains source and package identity, responses, native results and rubric judgments. Calibration is inside action-judgments.json, not a separate calibration.json file.

“Promotion and independent DEMO evidence are in the release artifact. A separately executed red-team scan has its own output. The workflows request 90-day retention; repository policy may limit it.

“Historical case files can be inspected now. Future v2 results must wait for actual executions.”""",
    16: """[SWITCH OUT: open the workflow and docs/RELEASE-GATE.md. Run the local gate tests, then inspect the historical candidate and DEMO release receipts.]

“We can show rejected stale checks, mismatched lineage and missing approval controls locally. Those tests are not a completed live PR gate.

“The historical release proves the original ZIP and v1 outcomes. New failed/passing live runs and v2 promotion remain pending.

[After approved activation, replace this route with actual run URLs and artifacts from the runbook. Do not approve or deploy as an improvised stage action.]""",
    17: """“Operation asks what happened and whether the release still meets its expectations. Traces help explain individual requests; evaluation measures defined criteria.

“Our prepared weekly workflow replays synthetic v1 cases against an explicitly pinned DEMO version. It is not enabled, it does not sample customer traffic, and it does not measure every action claim. Capture or scoring failures will require triage, not an automatic claim of a behavioral regression.

“Foundry Insights is a preview capability we can explain, but no Insights monitor was configured for this workshop.”""",
    18: """“The recorded DEMO answer said it was escalating to human support. There was no handoff tool. The answer nevertheless scored 1.0 under v1's decision, required-tool and reference checks.

“The response ID matches the saved trace. That is our genuine outer-loop finding, unlike the earlier DEV mismatch. The annotation is a reviewed repository record, not a native Insights finding.”""",
    19: """“A trace records what happened; a human supplies what should happen. Here the expectation is advice to contact support, not a claim that a handoff occurred.

“The two customer-language escalation cases and the action rubric make that expectation reviewable. Replaying the historical response proves that v1 missed the claim and the local v2 regression catches it.

“The code repair then needs the same separately activated release gate. AI-written changes do not get a different standard.”""",
    20: """[SWITCH OUT: open the recorded DEMO response, matching trace and recordings/escalation-finding.json. Show the two new dataset cases.]

[Run the recorded-finding regression and the actual Agent/Responses-host tests from the runbook. Show the repair diff, not a fabricated live pass.]

“This is real recorded evidence and a local fail/fix/pass demonstration. The new cloud gate, calibration and promotion are still pending. The prepared weekly v1 check alone would not have detected this missing semantic criterion.”""",
    21: """“Each row is a deliberate architecture choice. Hosted code lets us enforce the contract; curated tools narrow the capability set; IQ retrieval remains inspectable.

“The final renderer cites references supplied by business tools, not arbitrary model prose. Backend authorization is still required. Release and scheduled checks are implemented but awaiting cloud activation and proof.

“The feedback path is the part to take into a customer's design review: an observed failure becomes a reviewed test before the next release.”""",
    24: """Q&A: use the backup slides only when relevant.

Why a model? It understands the request and chooses tools; code owns the final business decision.
Are eleven cases enough? They are a regression suite, not a production-readiness certificate.
Does the live gate run now? Credential-free checks run; cloud evaluation and promotion require separate activation and approvals.
Is this hard production isolation? No: DEV and DEMO share an account.
Where is the red-team scorecard? No scan has completed; SDK installation is currently blocked.
Memory? Historical one-caller DEV proof exists. Cross-user isolation and the revised Memory-enabled response UX are not cloud-verified.""",
    25: "Backup only. Explain synthetic data, bounded coverage, shared-account isolation limits, preview status and pending cloud evidence. No SLA, regional-processing or universal-safety promise.",
    26: "Backup only. Historical Memory proof covered one authenticated DEV caller; Memory remains off in DEMO. The revised contract is always installed, so Memory-only requests return unavailable without business evidence. Do not imply the old cloud receipt verifies the revised UX.",
}


def replace_text(slide, shape_id, text):
    shape = next(s for s in slide.shapes if s.shape_id == shape_id)
    frame = shape.text_frame
    paragraph = frame.paragraphs[0]
    paragraph_properties = deepcopy(paragraph._p.pPr)
    run_properties = next((deepcopy(r._r.rPr) for r in paragraph.runs if r._r.rPr is not None), None)
    frame.clear()
    for index, line in enumerate(text.split("\n")):
        p = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        if paragraph_properties is not None:
            if p._p.pPr is not None:
                p._p.remove(p._p.pPr)
            p._p.insert(0, deepcopy(paragraph_properties))
        run = p.add_run()
        run.text = line
        if run_properties is not None:
            run._r.insert(0, deepcopy(run_properties))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=OUTPUT)
    args = parser.parse_args()
    deck = Presentation(args.source)
    if len(deck.slides) != 26:
        raise ValueError("Expected the approved 26-slide source, not a historical workshop.")
    manuscript = [
        "# Presenter guide — Can we defend this release?",
        "Current 26-slide deck: 24 visible slides and two hidden backups. "
        "These are the deck's speaker notes and operating cues; detailed demo commands live in docs/DEMO-RUNBOOK.md. "
        "Historical cloud evidence and local tests are distinct from pending v2 cloud activation.",
        "**Demo entry/return pairs:** 8/9, 13/14, 16/17, 20/21. "
        "Content ends at 80:00; Q&A runs to 90:00. No deployment, permission change or new paid run is implied.",
    ]
    for n, slide in enumerate(deck.slides, 1):
        slide._element.set("show", "0" if n > 24 else "1")
        for shape in slide.shapes:
            if shape.has_text_frame:
                frame = shape.text_frame
                while len(frame.paragraphs) > 1 and not frame.paragraphs[-1].text.strip():
                    frame._txBody.remove(frame.paragraphs[-1]._p)
        for shape_id, text in REPLACEMENTS.get(n, {}).items():
            replace_text(slide, shape_id, text)
        if n == 9:
            statistic = next(s for s in slide.shapes if s.shape_id == 21696)
            for paragraph in statistic.text_frame.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(90)
        if n in DEMOS:
            back, shape_id = DEMOS[n]
            replace_text(slide, shape_id, f"RETURN TO SLIDE {back:02} · Cloud steps pending: use local / recorded evidence · 30-second fallback cutoff")
        title_shape = next((s for s in slide.shapes if s.has_text_frame and s.text.strip()), None)
        texts = [s.text.strip() for s in slide.shapes if s.has_text_frame and s.text.strip()]
        title = texts[1] if n != 24 else title_shape.text.strip()
        original = slide.notes_slide.notes_text_frame.text.split("\n[DELIVERY CLOCK]", 1)[0].strip()
        original = re.sub(r"^\[\d+:\d+.*?\]\s*", "", original)
        note = NOTES.get(n, original)
        if n <= 24:
            start, end = CLOCKS[n - 1]
            clock = f"**Clock {start:02}:00–{end:02}:00"
            clock += " · 1 minute transitions.**" if n in DEMOS else ".**"
        else:
            clock = "**Hidden Q&A backup.**"
        if n in DEMOS:
            note += f"\n\n[RETURN: come back to this card and advance once to slide {DEMOS[n][0]}.]"
        slide.notes_slide.notes_text_frame.text = note + "\n[DELIVERY CLOCK]\n" + clock
        manuscript.append(f"## Slide {n:02} — {title}\n\n{clock}\n\n{note}")
    deck.save(OUTPUT)
    (ROOT / "Presenter manuscript.md").write_text("\n\n".join(manuscript) + "\n", encoding="utf-8")
    print(f"Prepared {OUTPUT.name}: 26 slides; 24 visible, backups 25–26.")


if __name__ == "__main__":
    main()
