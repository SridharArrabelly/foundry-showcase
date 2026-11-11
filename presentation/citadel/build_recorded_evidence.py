"""Build a small offline viewer from explicitly whitelisted, read-only exports."""
from __future__ import annotations

import base64
import hashlib
import json
import math
import re
from pathlib import Path
from urllib.parse import urlsplit

HERE = Path(__file__).parent
DEMO = HERE.parents[1]
SPECS = [
    ("baseline-v1", "DEV baseline · v1", "volt-dev", "1", (8, 1, 0, 9)),
    ("candidate-v6", "DEV candidate · v6", "volt-dev", "6", (9, 0, 0, 9)),
    ("demo-v1", "Released DEMO · v1", "volt-demo", "1", (9, 0, 0, 9)),
]
OPTIMIZER_REPORT = (
    "https://ai.azure.com/nextgen/r/QLaHyjG1Q3S-okwXg2m5wA,rg-volt-citadel,,"
    "fdy-volt-citadel-261111,volt-dev/build/agents/volt-support/optimization/"
    "opt_bcc5008122ae4a88ab10bfa428ecf616"
)


def safe_text(value: object, limit: int = 12000) -> str:
    if value is None:
        return ""
    if not isinstance(value, (str, int, float, bool)):
        raise ValueError("Only scalar display values may leave an evidence source.")
    text = str(value)
    if len(text) > limit:
        raise ValueError("Unexpectedly large display field.")
    # Never carry a signed/download link through an answer or citation field.
    def redact(match: re.Match[str]) -> str:
        link = match.group(0)
        parts = urlsplit(link)
        if parts.query or parts.fragment or re.search(
            r"download|blob\.core\.windows\.net|[?&](sig|token|se|sp|sv)=",
            link, re.IGNORECASE,
        ):
            return "[recorded link omitted]"
        return link
    return re.sub(r"https?://[^\s<>\"'\]]+", redact, text)


def report_link(value: str, kind: str) -> str:
    parts = urlsplit(value)
    required = "/build/evaluations/" if kind == "evaluation" else "/optimization/"
    if (
        parts.scheme != "https" or parts.netloc != "ai.azure.com"
        or not parts.path.startswith("/nextgen/r/") or required not in parts.path
        or parts.query or parts.fragment or parts.username or parts.password
        or "download" in parts.path.lower()
    ):
        raise ValueError("Only canonical, unsigned native report links are allowed.")
    return value


def number(value: object) -> float | int:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("Invalid recorded number.")
    return value


def read_source(path: Path, manifest: list[dict]) -> dict:
    raw = path.read_bytes()
    manifest.append({"path": str(path.relative_to(DEMO)), "sha256": hashlib.sha256(raw).hexdigest()})
    data = json.loads(raw.decode("utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected an object in {path.name}")
    return data


def extract_case(row: dict) -> dict:
    case = row["case"]
    ident = case["id"]
    if not re.fullmatch(r"[a-z0-9-]+", ident):
        raise ValueError("Unexpected case identifier.")
    answer = json.loads(row["output_text"])
    if not isinstance(answer, dict) or not isinstance(answer.get("answer"), str):
        raise ValueError("Expected the captured structured answer.")
    outputs = {
        item.get("call_id"): item for item in row.get("protocol_output", [])
        if item.get("type") == "function_call_output"
    }
    tools = []
    for item in row.get("protocol_output", []):
        if item.get("type") != "function_call" or not isinstance(item.get("name"), str):
            continue
        output = outputs.get(item.get("call_id"), {})
        tools.append({
            "name": safe_text(item["name"], 300),
            "protocol_status": safe_text(output.get("status", item.get("status", "not recorded")), 80),
        })
    citations = []
    for citation in answer.get("citations", []):
        if not isinstance(citation, dict):
            raise ValueError("Unexpected citation shape.")
        citations.append({
            "reference": safe_text(citation.get("reference"), 500),
            "title": safe_text(citation.get("title"), 1000),
        })
    return {
        "id": ident,
        "query": safe_text(case["query"]),
        "expected_decision": safe_text(case["expected_decision"], 120),
        "actual_decision": safe_text(answer.get("decision"), 120),
        "required_tool": safe_text(case.get("required_tool"), 300),
        "expected_reference": safe_text(case.get("expected_reference"), 500),
        "answer": safe_text(answer["answer"]),
        "citations": citations,
        "tools": tools,
    }


def build_payload() -> tuple[dict, list[dict]]:
    manifest: list[dict] = []
    runs = []
    evaluator_hashes = set()
    for ident, label, project, version, expected_counts in SPECS:
        source = read_source(DEMO / "showcase" / "recordings" / f"{ident}.json", manifest)
        if source["kind"] != "recorded-synthetic-evidence":
            raise ValueError("Not a recorded synthetic export.")
        if not source["project_endpoint"].endswith("/api/projects/" + project):
            raise ValueError("Recording project does not match the declared run.")
        counts = {key: int(number(source["native_counts"][key]))
                  for key in ["passed", "failed", "errored", "total", "skipped"]}
        if tuple(counts[k] for k in ["passed", "failed", "errored", "total"]) != expected_counts:
            raise ValueError("Native counts differ from the verified result; review before publishing.")
        if counts["total"] != len(source["cases"]) or sum(
            counts[k] for k in ["passed", "failed", "errored", "skipped"]
        ) != counts["total"]:
            raise ValueError("Counts and capture coverage disagree.")
        for row in source["cases"]:
            if str(row["agent_reference"]["version"]) != version:
                raise ValueError("Unexpected agent version in business captures.")
        evaluator_hashes.add(source["evaluator_sha256"])
        cases = [extract_case(row) for row in source["cases"]]
        if len({c["id"] for c in cases}) != len(cases):
            raise ValueError("Duplicate case.")
        runs.append({
            "id": ident, "label": label, "project": project, "version": version,
            "source_name": f"{ident}.json", "counts": counts,
            "evaluator_version": safe_text(source["evaluator_version"], 30),
            "report_url": report_link(source["report_url"], "evaluation"),
            "failed_invocation_attempts": len(source.get("failed_invocation_attempts", [])),
            "cases": cases,
        })
    if len(evaluator_hashes) != 1:
        raise ValueError("The exports do not use the same pinned evaluator hash.")
    expected_cases = [{k: c[k] for k in ["id", "query", "expected_decision", "required_tool", "expected_reference"]}
                      for c in runs[0]["cases"]]
    for run in runs[1:]:
        if expected_cases != [{k: c[k] for k in expected_cases[0]} for c in run["cases"]]:
            raise ValueError("Case definitions differ across captures.")

    source = read_source(DEMO / "showcase" / "recordings" / "optimizer.json", manifest)
    if (
        source["kind"] != "recorded-native-optimizer-outcome"
        or source["report_url"] != OPTIMIZER_REPORT
        or source["accepted_optimized_candidate"] is not False
        or source["applied_candidate"] is not False
    ):
        raise ValueError("Unexpected portable Optimizer recording.")
    budget = source["requested_max_candidates"]
    if (source["status"], source["termination_reason"], source["completed_candidate_count"],
        source["baseline_score"], source["best_score"], budget) != (
        "succeeded", "candidate_screening_stalled", 0, .75, .75, 2
    ):
        raise ValueError("Optimizer outcome changed; do not automatically reinterpret it.")
    optimizer = {
        "status": safe_text(source["status"], 80),
        "termination": safe_text(source["termination_reason"], 120),
        "baseline_score": number(source["baseline_score"]),
        "best_score": number(source["best_score"]),
        "completed_candidates": int(number(source["completed_candidate_count"])),
        "maximum_candidate_budget": int(number(budget)),
        # Previously verified warning text; the portable record preserves the same terminal facts.
        "warnings": [
            "Optimizer returned only the baseline; no optimized candidates were generated.",
            "Optimization stopped after reaching the maximum consecutive stall limit with no improvement.",
        ],
        "report_url": report_link(source["report_url"], "optimization"),
        "decision": "Baseline retained. No accepted improvement. Nothing applied.",
        "deploy_warning": "Do not click “Deploy best candidate” in the portal: it would deploy the retained baseline, not an improved candidate.",
    }

    source = read_source(DEMO / "showcase" / "recordings" / "demo-trace.json", manifest)
    spans = source["spans"]
    root = "7f4619cba4075a99c6d1b077dad68f69"
    response = "caresp_03f2cedafe9a81ff00ml4CEH7VZPqFrxR1SFFHpglDzRb3u45a"
    if source["response_id"] != response or len(spans) != 43 or any(s["operation_Id"] != root for s in spans):
        raise ValueError("Fresh DEMO correlation export differs from the verified proof.")
    trace = {
        "span_count": len(spans),
        "operation_id": root,
        "response_id": response,
        "project": "volt-demo", "version": 1,
        "timestamp_utc": "2026-11-11T17:19:09.3446407Z",
        "root_duration_seconds": 23.4094,
        "scope": "A separate fresh golden DEMO request—not the historical incident.",
        "baseline_limit": "The old incident’s reported correlation ID was not found in exported App Insights. Its proof is native capture/tool sequence plus failed native evaluation.",
        "spans": [{
            "name": safe_text(s["name"], 500),
            "duration_ms": number(s["duration"]),
            "success": safe_text(s.get("success"), 30),
        } for s in spans],
    }
    payload = {
        "runs": runs, "optimizer": optimizer, "trace": trace,
        "disclosures": [
            "RECORDED EVIDENCE — NOT LIVE. These are retained real synthetic responses, not a live runtime or portal screenshot.",
            "Native counts grade completed captures. They do not rerun the agent and are not an availability guarantee.",
            "One initial DEV candidate model-service invocation failed, was preserved, and was retried once.",
            "DEMO’s 9/9 is its own native evaluator v1 result on nine fresh runtime cases—not a reused DEV result.",
            "Memory data is intentionally omitted: one-caller DEV v5 proof exists, but cross-user isolation is unproved; DEMO Memory is off.",
            "No automatic Insights monitor/findings or completed human 90-minute timing rehearsal is claimed.",
        ],
    }
    for item in manifest:
        if hashlib.sha256((DEMO / item["path"]).read_bytes()).hexdigest() != item["sha256"]:
            raise RuntimeError("A source changed during generation; retry from a consistent snapshot.")
    return payload, manifest


THEME_JS = """(() => {
    const param = new URLSearchParams(window.location.search).get("scoutTheme");
    const theme =
      param || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
    document.documentElement.setAttribute("data-theme", theme);
  })();"""

CSS = """
:root {
  color-scheme: light;
  --cp-bg: #f7f4ef;
  --cp-bg-elevated: #fcfbf8;
  --cp-surface: #ffffff;
  --cp-surface-soft: #f5f5f5;
  --cp-border: #dedede;
  --cp-border-strong: #919191;
  --cp-text: #242424;
  --cp-text-muted: #5c5c5c;
  --cp-text-soft: #6f6f6f;
  --cp-accent: #b11f4b;
  --cp-accent-hover: #9a1a41;
  --cp-accent-soft: rgba(177, 31, 75, 0.08);
  --cp-accent-fg: #ffffff;
  --cp-success: #16a34a;
  --cp-danger: #dc2626;
  --cp-warning: #f59e0b;
  --cp-link: #0078d4;
  --cp-shadow: 0 18px 48px rgba(0, 0, 0, 0.12);
  --cp-overlay: rgba(255, 255, 255, 0.8);
  --cp-panel: rgba(255, 255, 255, 0.86);
  --cp-panel-strong: rgba(255, 255, 255, 0.96);
  --cp-sheen: rgba(255, 255, 255, 0.55);
  --cp-highlight: rgba(177, 31, 75, 0.12);
}
html[data-theme="dark"] {
  color-scheme: dark;
  --cp-bg: #3d3b3a;
  --cp-bg-elevated: #343231;
  --cp-surface: #292929;
  --cp-surface-soft: #2e2e2e;
  --cp-border: #474747;
  --cp-border-strong: #5f5f5f;
  --cp-text: #dedede;
  --cp-text-muted: #919191;
  --cp-text-soft: #b0b0b0;
  --cp-accent: #fd8ea1;
  --cp-accent-hover: #fb7b91;
  --cp-accent-soft: rgba(253, 142, 161, 0.14);
  --cp-accent-fg: #1a1a1a;
  --cp-success: #4ade80;
  --cp-danger: #f87171;
  --cp-warning: #fbbf24;
  --cp-link: #4da6ff;
  --cp-shadow: 0 18px 48px rgba(0, 0, 0, 0.32);
  --cp-overlay: rgba(41, 41, 41, 0.88);
  --cp-panel: rgba(41, 41, 41, 0.72);
  --cp-panel-strong: rgba(41, 41, 41, 0.96);
  --cp-sheen: rgba(255, 255, 255, 0.04);
  --cp-highlight: rgba(253, 142, 161, 0.12);
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--cp-bg); color: var(--cp-text);
  font: 17px/1.5 "Segoe UI", Aptos, Calibri, -apple-system, BlinkMacSystemFont, sans-serif; }
.banner { background: var(--cp-accent); color: var(--cp-accent-fg); padding: 16px 24px;
  font-size: 18px; font-weight: 750; text-align: center; letter-spacing: .06em; }
main { max-width: 1240px; margin: auto; padding: 28px 24px 40px; }
.eyebrow { color: var(--cp-text-muted); font-weight: 650; font-size: 13px; letter-spacing: .08em; }
h1 { font-size: clamp(28px, 3.2vw, 42px); line-height: 1.15; margin: 8px 0; }
h2 { font-size: 23px; line-height: 1.25; margin: 0 0 12px; }
h3 { font-size: 16px; margin: 18px 0 8px; }
p { margin: 8px 0; } a { color: var(--cp-link); overflow-wrap: anywhere; }
.muted, .fine { color: var(--cp-text-muted); } .fine { font-size: 13px; }
.stats { display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: 16px; margin: 24px 0; }
.stat, .panel, .question, .optimizer, .observability {
  background: var(--cp-surface); border: 1px solid var(--cp-border); border-radius: 16px; padding: 20px; min-width: 0;
}
.stat h2 { font-size: 18px; } .score { font-size: 38px; font-weight: 750; line-height: 1.2; }
.stat p { font-size: 14px; } .stat a { font-size: 14px; font-weight: 600; }
.controls { display: flex; flex-wrap: wrap; gap: 16px; margin: 12px 0 20px; align-items: end; }
.control { flex: 1 1 280px; } label { display: block; font-size: 14px; font-weight: 650; margin-bottom: 6px; }
select { width: 100%; padding: 12px; border: 1px solid var(--cp-border-strong); border-radius: .625rem;
  background: var(--cp-surface); color: var(--cp-text); font: inherit; }
select:focus-visible, a:focus-visible, summary:focus-visible { outline: 3px solid var(--cp-link); outline-offset: 3px; }
.question { background: var(--cp-bg-elevated); margin-bottom: 16px; }
.question p { font-size: 17px; } .compare { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 16px; }
.verdict { display: inline-block; padding: 4px 10px; border: 1px solid var(--cp-border);
  border-radius: .625rem; font-size: 13px; font-weight: 650; margin-bottom: 12px; }
.mismatch { color: var(--cp-danger); border-color: var(--cp-danger); }
.match { color: var(--cp-text); background: var(--cp-surface-soft); }
.decisions { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding-bottom: 12px; }
.field-label { display: block; color: var(--cp-text-muted); font-size: 13px; }
.decision { font-size: 20px; font-weight: 700; overflow-wrap: anywhere; }
.answer { white-space: pre-wrap; overflow-wrap: anywhere; line-height: 1.55; margin: 12px 0; }
.citations, .tools { margin: 4px 0; padding-left: 20px; font-size: 14px; overflow-wrap: anywhere; }
.citations li, .tools li { margin-bottom: 4px; }
.tools { font-family: Consolas, "Courier New", Courier, monospace; font-size: 14px; }
.optimizer, .observability { margin-top: 20px; }
.optimizer { background: var(--cp-bg-elevated); }
.opt-metrics { display: flex; gap: 12px 28px; flex-wrap: wrap; margin: 12px 0; }
.opt-metrics strong { display: block; font-size: 24px; }
.warning { padding: 12px 16px; border-radius: .625rem; background: var(--cp-accent-soft); color: var(--cp-text); font-weight: 600; }
code { font-family: Consolas, "Courier New", Courier, monospace; overflow-wrap: anywhere; font-size: .88em; }
summary { cursor: pointer; font-weight: 650; padding: 12px 0; }
.span-scroll { max-height: 340px; overflow: auto; }
table { border-collapse: collapse; width: 100%; font-size: 13px; }
th, td { padding: 8px; border-bottom: 1px solid var(--cp-border); text-align: left; overflow-wrap: anywhere; }
th { background: var(--cp-surface-soft); }
footer { margin-top: 24px; font-size: 13px; color: var(--cp-text-muted); }
footer li { margin: 6px 0; }
@media(max-width: 760px) { main { padding: 20px 16px; } .stats, .compare { grid-template-columns: 1fr; }
  .banner { font-size: 15px; padding: 12px; } .stat { padding: 16px; } .score { font-size: 30px; } }
@media(max-width: 460px) { .decisions { grid-template-columns: 1fr; } }
@media print { .banner { position: static; } .controls { display: none; } body { background: var(--cp-surface); }
  main { padding: 12px; } .panel, .stat, .optimizer { break-inside: avoid; } }
"""

APP_JS = r"""(() => {
  "use strict";
  const data = JSON.parse(document.getElementById("recorded-data").textContent);
  const byId = Object.fromEntries(data.runs.map(run => [run.id, run]));
  const create = (tag, text, cls) => {
    const node = document.createElement(tag);
    if (text !== undefined) node.textContent = String(text);
    if (cls) node.className = cls;
    return node;
  };
  const link = (label, url) => {
    const node = create("a", label);
    node.href = url; node.target = "_blank"; node.rel = "noopener noreferrer";
    return node;
  };
  const set = (id, value) => { document.getElementById(id).textContent = String(value); };
  for (const run of data.runs) {
    const card = create("section", undefined, "stat");
    card.dataset.run = run.id;
    card.append(create("h2", run.label), create("div", `${run.counts.passed}/${run.counts.total}`, "score"));
    card.append(create("p", `${run.counts.failed} failed · ${run.counts.errored} errored · ${run.counts.skipped} skipped`, "muted"));
    card.append(link("Open actual native report ↗", run.report_url));
    if (run.failed_invocation_attempts) card.append(create("p", `${run.failed_invocation_attempts} earlier invocation failure preserved; retried once. Business score ≠ availability.`, "fine"));
    document.getElementById("stats").append(card);
  }
  const chooser = document.getElementById("case-select");
  for (const c of data.runs[0].cases) {
    const option = create("option", c.id); option.value = c.id; chooser.append(option);
  }
  const runChooser = document.getElementById("run-select");
  for (const run of data.runs.slice(1)) {
    const option = create("option", run.label); option.value = run.id; runChooser.append(option);
  }
  chooser.value = "replacement-recall"; runChooser.value = "demo-v1";
  function renderPanel(id, run, c) {
    const panel = document.getElementById(id);
    panel.replaceChildren();
    panel.append(create("h2", run.label));
    const equal = c.expected_decision === c.actual_decision;
    panel.append(create("div", equal ? "Decision matches expected" : "Decision mismatch", `verdict ${equal ? "match" : "mismatch"}`));
    const fields = create("div", undefined, "decisions");
    for (const [label, value] of [["Expected decision", c.expected_decision], ["Actual decision", c.actual_decision]]) {
      const field = create("div");
      field.append(create("span", label, "field-label"), create("span", value || "Not recorded", "decision"));
      fields.append(field);
    }
    panel.append(fields, create("p", "This comparison is the decision field, not a substitute for the complete native evaluator.", "fine"));
    panel.append(create("h3", "Captured human-readable answer"), create("p", c.answer, "answer"));
    panel.append(create("h3", "Citations in the recorded answer"));
    const citations = create("ul", undefined, "citations");
    for (const cite of c.citations) citations.append(create("li", [cite.reference, cite.title].filter(Boolean).join(" — ")));
    if (!c.citations.length) citations.append(create("li", "No citations in this captured answer."));
    panel.append(citations, create("h3", "Tools in the native protocol sequence"));
    const tools = create("ol", undefined, "tools");
    for (const tool of c.tools) tools.append(create("li", `${tool.name} · ${tool.protocol_status}`));
    if (!c.tools.length) tools.append(create("li", "No function calls in this capture."));
    panel.append(tools, create("p", `Source: ${run.source_name} · ${run.project} · agent version ${run.version} · evaluator v${run.evaluator_version}`, "fine"));
  }
  function render() {
    const baseline = byId["baseline-v1"];
    const comparison = byId[runChooser.value];
    const c = baseline.cases.find(item => item.id === chooser.value);
    set("case-query", c.query);
    set("case-requirements", `Required tool: ${c.required_tool || "none specified"} · Expected source: ${c.expected_reference || "none required"}`);
    renderPanel("baseline-panel", baseline, c);
    renderPanel("comparison-panel", comparison, comparison.cases.find(item => item.id === chooser.value));
  }
  chooser.addEventListener("change", render); runChooser.addEventListener("change", render); render();
  const opt = data.optimizer;
  set("opt-status", `${opt.status} · ${opt.termination}`);
  set("opt-decision", opt.decision);
  set("opt-baseline", opt.baseline_score);
  set("opt-best", opt.best_score);
  set("opt-completed", opt.completed_candidates);
  set("opt-budget", opt.maximum_candidate_budget);
  set("opt-warning", opt.deploy_warning);
  const warnings = document.getElementById("opt-warnings");
  for (const warning of opt.warnings) warnings.append(create("li", warning));
  document.getElementById("opt-link").append(link("Open completed native Optimizer report ↗", opt.report_url));
  const trace = data.trace;
  set("trace-summary", `${trace.span_count} verified correlated spans · ${trace.project} · v${trace.version} · ${trace.root_duration_seconds}s root duration (one observation, not an SLA)`);
  set("trace-boundary", trace.scope + " " + trace.baseline_limit);
  set("trace-ids", `Fresh response: ${trace.response_id}\nRoot operation: ${trace.operation_id}\nUTC: ${trace.timestamp_utc}`);
  const body = document.getElementById("span-rows");
  for (const span of trace.spans) {
    const row = create("tr");
    row.append(create("td", span.name), create("td", (span.duration_ms / 1000).toFixed(4) + " s"), create("td", span.success || "not recorded"));
    body.append(row);
  }
  for (const note of data.disclosures) document.getElementById("disclosures").append(create("li", note));
  document.documentElement.dataset.ready = "true";
})();"""


def script_hash(script: str) -> str:
    return base64.b64encode(hashlib.sha256(script.encode("utf-8")).digest()).decode("ascii")


def safe_json_embed(payload: dict) -> str:
    return (json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
            .replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
            .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))


def render_document(payload: dict) -> str:
    csp = ("default-src 'none'; script-src 'sha256-" + script_hash(THEME_JS)
           + "' 'sha256-" + script_hash(APP_JS)
           + "'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; "
           "font-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{csp}">
<title>Volt & Co — Recorded evidence, not live</title>
<script>{THEME_JS}</script><style>{CSS}</style></head>
<body>
<div class="banner">RECORDED EVIDENCE — NOT LIVE</div>
<main>
<header><div class="eyebrow">VOLT & CO / MICROSOFT FOUNDRY / CITADEL</div>
<h1>One case. Evidence across the release.</h1>
<p class="muted">Real captured synthetic answers and native business grading. Works offline; report links open online only if you choose them.</p></header>
<div id="stats" class="stats" aria-label="Actual native evaluation counts"></div>
<div class="controls">
<div class="control"><label for="case-select">Recorded case</label><select id="case-select"></select></div>
<div class="control"><label for="run-select">Compare the baseline with</label><select id="run-select"></select></div>
</div>
<section class="question"><h2>Customer request</h2><p id="case-query"></p><p id="case-requirements" class="fine"></p></section>
<div class="compare"><section id="baseline-panel" class="panel"></section><section id="comparison-panel" class="panel"></section></div>
<p class="fine">Synthetic, read-only support demonstration. The answer is actual captured model text; it does not prove a refund, shipment, order mutation or external hand-off occurred.</p>
<section class="optimizer"><h2>Optimizer: no improvement</h2><p id="opt-decision"></p><p id="opt-status" class="fine"></p>
<div class="opt-metrics"><div><span class="field-label">Baseline task-adherence</span><strong id="opt-baseline"></strong></div>
<div><span class="field-label">Best task-adherence</span><strong id="opt-best"></strong></div>
<div><span class="field-label">Completed candidates</span><strong id="opt-completed"></strong></div>
<div><span class="field-label">Maximum budget—not completed</span><strong id="opt-budget"></strong></div></div>
<p id="opt-warning" class="warning"></p><ul id="opt-warnings" class="fine"></ul><div id="opt-link"></div>
<p class="fine">The separate business-contract code fix was locally Copilot-assisted and reviewed through PR #2. It was not an Optimizer-applied candidate.</p></section>
<section class="observability"><h2>Fresh DEMO observability—separate proof</h2><p id="trace-summary"></p><p id="trace-boundary" class="fine"></p>
<details><summary>Inspect the 43 recorded correlated spans</summary><p id="trace-ids" class="fine answer"></p>
<div class="span-scroll"><table><thead><tr><th>Recorded span name</th><th>Duration</th><th>Recorded success</th></tr></thead><tbody id="span-rows"></tbody></table></div></details>
<p class="fine">Correlation uses azure.ai.agentserver.response_id; version uses gen_ai.agent.version; project uses microsoft.foundry.project.id. gen_ai.agent.id is a principal GUID, not name:version.</p></section>
<footer><details><summary>Evidence boundaries and provenance</summary><ul id="disclosures"></ul>
<p>No fetch, CDN, server, analytics or private Memory data. No signed portal download URLs. The source generator keeps only explicit display fields; system prompts, credentials, tool arguments and raw telemetry properties are not embedded.</p></details></footer>
<noscript>This recorded viewer requires local JavaScript. No server or network is required.</noscript>
</main><script type="application/json" id="recorded-data">{safe_json_embed(payload)}</script>
<script>{APP_JS}</script></body></html>"""


def main() -> None:
    payload, manifest = build_payload()
    output = HERE / "Recorded evidence.html"
    output.write_text(render_document(payload), encoding="utf-8")
    (HERE / "recorded-evidence-manifest.json").write_text(json.dumps({
        "output": output.name,
        "inputs_read_only": manifest,
        "runs": [{"name": r["label"], "counts": r["counts"]} for r in payload["runs"]],
        "memory_included": False,
        "signed_download_urls_included": False,
        "raw_protocol_or_telemetry_properties_included": False,
    }, indent=2), encoding="utf-8")
    print(output)
    print(f"{output.stat().st_size:,} bytes; 3 runs / 27 captures; 43 whitelisted span rows; no external dependencies.")


if __name__ == "__main__":
    main()
