"""Generate a credential-free, offline-readable fallback from actual captured runs."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"


def escaped(value):
    return html.escape(str(value))


def load(name):
    path = EVIDENCE / name
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def main():
    sections = []
    for label, name in [("Baseline", "baseline.json"), ("Improved candidate", "candidate.json")]:
        data = load(name)
        if not data:
            sections.append(f"<section><h2>{label}</h2><p>No recorded result available.</p></section>")
            continue
        rows = []
        for case in data["cases"]:
            result = case["result"]
            state = "PASS" if case["passed"] else "FAIL"
            tools = " > ".join(call["name"] for call in result["tool_calls"])
            rows.append(
                f"<tr><td>{escaped(case['id'])}</td><td class='{state.lower()}'>{state}</td>"
                f"<td>{escaped(result['output']['decision'])}</td><td>{escaped(tools)}</td></tr>"
            )
        sections.append(
            f"<section><h2>{label}: {data['passed']}/{data['total']} reviewed cases</h2>"
            f"<p>Recorded {escaped(data['created_at'])} | Hosted version {escaped(data['requested_version'])}</p>"
            "<table><tr><th>Case</th><th>Result</th><th>Decision</th><th>Observed tool calls</th></tr>"
            + "".join(rows) + "</table><p>Small synthetic dataset. Not an accuracy benchmark or safety certification.</p></section>"
        )
    trace = load("missing-batch-baseline.json")
    if trace:
        sections.append(
            "<section><h2>The feedback moment</h2><p>I have a Volt Charge 65. Is it safe?</p>"
            f"<blockquote>{escaped(trace['output']['answer'])}</blockquote>"
            f"<p>Decision: <strong>{escaped(trace['output']['decision'])}</strong>; "
            f"trace: <code>{escaped(trace.get('trace_id'))}</code></p>"
            "<p>The defect: a missing batch became a negative lookup. Human-reviewed expectation: ask for the batch.</p>"
            f"<details><summary>Actual tool evidence</summary><pre>{escaped(json.dumps(trace['tool_calls'], indent=2))}</pre></details></section>"
        )
    links = []
    for label, name in [("Baseline coherence", "foundry-baseline-evaluation.json"),
                        ("Candidate coherence", "foundry-evaluation.json")]:
        result = load(name)
        if result:
            links.append(f"<li><a href='{escaped(result['report_url'])}'>{label}</a>: {escaped(result['status'])}</li>")
    sections.append("<section><h2>Native Foundry model-judged scorecards</h2><ul>"
                    + "".join(links) + "</ul><p>Coherence of captured live outputs, not domain correctness or replay.</p></section>")
    release = load("release.json")
    if release:
        sections.append("<section><h2>Approved demo-client release pointer</h2><pre>"
                        + escaped(json.dumps(release, indent=2)) + "</pre></section>")
    output = """<!doctype html><html lang="en"><meta charset="utf-8"><title>Volt & Co | Recorded evidence</title>
<style>body{font:18px/1.5 'Segoe UI',sans-serif;background:#f7f7fa;color:#242424;margin:0}
header{background:#1c1b30;color:white;padding:48px max(5vw,24px)}main{max-width:1180px;margin:auto;padding:24px}
h1{font-size:38px;margin:0}h2{font-size:26px;color:#0408ac}section{background:white;border:1px solid #d8d5e9;border-radius:16px;padding:24px;margin:24px 0}
table{border-collapse:collapse;width:100%;font-size:15px}th,td{text-align:left;padding:12px;border-bottom:1px solid #e6e1ff}
th{background:#e6e1ff}.pass{color:#087a54;font-weight:bold}.fail{color:#b3261e;font-weight:bold}
pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px;background:#f7f7fa;padding:16px}
.badge{background:#4f42fd;display:inline-block;padding:6px 12px;border-radius:20px;font-size:14px}
a{color:#0408ac}blockquote{border-left:4px solid #4f42fd;padding:8px 20px}</style>
<header><span class="badge">RECORDED LIVE EVIDENCE | NOT A LIVE DASHBOARD</span><h1>Volt & Co: the evidence trail</h1>
<p>GitHub Copilot SDK to Microsoft Foundry. Synthetic data, actual captured responses.</p></header><main>"""
    target = ROOT / "presentation" / "Recorded demo evidence.html"
    target.write_text(output + "".join(sections) + "</main></html>", encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
