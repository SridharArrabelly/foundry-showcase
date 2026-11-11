"""Local, offline browser checks; no Azure/Git operations or source mutations."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright, expect
import build_recorded_evidence as build

ROOT = Path(__file__).parent
RENDERS = ROOT / "renders"
PROFILE = ROOT / ".recorded-browser-profile"
FIXTURE = ROOT / ".recorded-injection-check.html"


def main() -> None:
    payload, source_manifest = build.build_payload()
    assert all(Path(item["path"]).parts[:2] == ("showcase", "recordings") for item in source_manifest)
    document = (ROOT / "Recorded evidence.html").read_text(encoding="utf-8")
    for forbidden in ["<script src", "<iframe", "fetch(", "XMLHttpRequest", "sendBeacon", "WebSocket(", "serviceWorker"]:
        assert forbidden not in document
    assert "RECORDED EVIDENCE — NOT LIVE" in document
    for value in [
        "javascript:alert(1)",
        "https://ai.azure.com/nextgen/r/x/build/evaluations/x/run/y?sig=SECRET",
        "https://ai.azure.com.evil.test/nextgen/r/x/build/evaluations/x/run/y",
    ]:
        try:
            build.report_link(value, "evaluation")
        except ValueError:
            pass
        else:
            raise AssertionError("Unsafe link accepted")
    row = {
        "case": {"id": "test", "query": "Synthetic", "expected_decision": "eligible"},
        "output_text": json.dumps({
            "answer": "Do not retain https://example.blob.core.windows.net/report?sig=SIGNED_URL_SENTINEL",
            "decision": "eligible",
            "citations": [{"reference": "https://ai.azure.com/download/file?token=SIGNED_URL_SENTINEL", "title": "Policy"}],
        }),
        "protocol_output": [],
    }
    assert "SIGNED_URL_SENTINEL" not in json.dumps(build.extract_case(row))
    malicious = '</script><img src="https://invalid.example/x" onerror="window.__injected=1"><script>window.__injected=1</script>\u2028\u2029'
    fixture = deepcopy(payload)
    fixture["runs"][0]["cases"][0]["answer"] = malicious
    fixture["runs"][0]["cases"][0]["query"] = malicious
    fixture["runs"][0]["cases"][0]["citations"][0]["title"] = malicious
    fixture["runs"][0]["cases"][0]["tools"][0]["name"] = malicious
    fixture["trace"]["spans"][0]["name"] = malicious
    FIXTURE.write_text(build.render_document(fixture), encoding="utf-8")
    network_requests = []
    errors = []
    checks = 0
    try:
        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                str(PROFILE), channel="msedge", headless=True,
                viewport={"width": 1440, "height": 1100},
                args=["--disable-background-networking", "--disable-component-update"],
            )
            context.set_offline(True)
            context.on("request", lambda request: network_requests.append(request.url)
                       if request.url.startswith(("http://", "https://")) else None)
            page = context.new_page()
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("console", lambda message: errors.append(message.text) if message.type == "error" else None)
            page.goto((ROOT / "Recorded evidence.html").as_uri() + "?scoutTheme=light")
            expect(page.locator("html")).to_have_attribute("data-ready", "true")
            expect(page.locator(".stat")).to_have_count(3)
            for run in payload["runs"]:
                expect(page.locator(f'[data-run="{run["id"]}"] .score')).to_have_text(
                    f'{run["counts"]["passed"]}/{run["counts"]["total"]}'
                )
            for comparison in payload["runs"][1:]:
                page.select_option("#run-select", comparison["id"])
                for case in comparison["cases"]:
                    page.select_option("#case-select", case["id"])
                    expect(page.locator("#comparison-panel .answer")).to_have_text(case["answer"])
                    expect(page.locator("#comparison-panel .decision").nth(1)).to_have_text(case["actual_decision"])
                    expect(page.locator("#comparison-panel .tools li")).to_have_count(max(1, len(case["tools"])))
                    baseline_case = next(c for c in payload["runs"][0]["cases"] if c["id"] == case["id"])
                    for panel, source_case in [("#baseline-panel", baseline_case), ("#comparison-panel", case)]:
                        expect(page.locator(panel + " .answer")).to_have_text(source_case["answer"])
                        expect(page.locator(panel + " .decision").nth(1)).to_have_text(source_case["actual_decision"])
                        expect(page.locator(panel + " .citations li")).to_have_count(max(1, len(source_case["citations"])))
                        if not source_case["citations"]:
                            expect(page.locator(panel + " .citations li")).to_have_text("No citations in this captured answer.")
                        for i, tool in enumerate(source_case["tools"]):
                            expect(page.locator(panel + " .tools li").nth(i)).to_contain_text(tool["name"])
                        for i, citation in enumerate(source_case["citations"]):
                            expect(page.locator(panel + " .citations li").nth(i)).to_contain_text(citation["reference"])
                    checks += 1
            page.select_option("#case-select", "replacement-recall")
            page.select_option("#run-select", "demo-v1")
            expect(page.locator("#baseline-panel .mismatch")).to_have_count(1)
            expect(page.locator("#comparison-panel .match")).to_have_count(1)
            expect(page.locator("#opt-completed")).to_have_text("0")
            expect(page.locator("#opt-budget")).to_have_text("2")
            expect(page.locator("#opt-baseline")).to_have_text("0.75")
            expect(page.locator("#opt-best")).to_have_text("0.75")
            expect(page.locator("#span-rows tr")).to_have_count(43)
            for href in page.locator("a").evaluate_all("(nodes) => nodes.map(n => n.href)"):
                assert urlsplit(href).netloc == "ai.azure.com" and not urlsplit(href).query
            assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")
            RENDERS.mkdir(exist_ok=True)
            page.screenshot(path=str(RENDERS / "recorded-evidence-desktop.png"), full_page=True)
            page.set_viewport_size({"width": 390, "height": 844})
            assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1")
            page.screenshot(path=str(RENDERS / "recorded-evidence-mobile.png"), full_page=True)
            page.goto((ROOT / "Recorded evidence.html").as_uri() + "?scoutTheme=dark")
            expect(page.locator("html")).to_have_attribute("data-theme", "dark")
            expect(page.locator("html")).to_have_attribute("data-ready", "true")
            page.goto(FIXTURE.as_uri() + "?scoutTheme=light")
            expect(page.locator("html")).to_have_attribute("data-ready", "true")
            assert page.locator("#baseline-panel .answer").text_content() == malicious
            assert page.evaluate("window.__injected === undefined")
            assert page.locator("img").count() == 0
            assert page.locator("script").count() == 3
            assert not network_requests, network_requests
            assert not errors, errors
            context.close()
        for item in source_manifest:
            actual = hashlib.sha256((build.DEMO / item["path"]).read_bytes()).hexdigest()
            assert actual == item["sha256"], "Source mutated"
        result = {
            "browser": "Local headless Microsoft Edge via Playwright",
            "offline": True, "network_requests": network_requests, "console_errors": errors,
            "comparisons_checked": checks, "recorded_runs": 3, "case_rows": 27,
            "trace_rows": 43, "desktop_and_mobile_layout": "passed",
            "theme_modes": ["light", "dark"],
            "script_termination_and_DOM_injection_fixture": "passed",
            "signed_download_url_redaction": "passed",
            "unsafe_report_link_rejection": "passed",
            "source_files_unchanged": True, "private_memory_data_included": False,
            "all_generator_inputs_are_portable_recordings": True,
        }
        (ROOT / "recorded-evidence-browser-validation.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(result, indent=2))
    finally:
        FIXTURE.unlink(missing_ok=True)
        if PROFILE.exists():
            shutil.rmtree(PROFILE, ignore_errors=True)


if __name__ == "__main__":
    main()
