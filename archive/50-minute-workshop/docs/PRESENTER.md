# Presenter operating guide

The complete, word-for-word delivery script is now:

- [Presenter script.md](../presentation/Presenter%20script.md): authored manuscript.
- [Presenter script.html](../presentation/Presenter%20script.html): readable,
  navigable and printable view for a second screen.
- [Presenter script.pdf](../presentation/Presenter%20script.pdf): print-ready
  reading copy. Copy commands from HTML or Markdown rather than PDF line wraps.
- The Notes pane of `Foundry - From prototype to operated service.pptx`: the same
  slide-specific script, embedded for PowerPoint Presenter View. Slide 1 also
  includes the pre-show setup at the end of its note.

## Delivery convention

Read **SAY**, **TRANSITION - SAY**, and **RETURN TO SLIDES - SAY** aloud.
Follow **DO**, **COMMAND**, **CHECK**, and **EXPECT** silently.
Conditional wording replaces the normal path; do not read every branch.
Only read success wording after observing the expected result.

The manuscript includes:

- The full 00:00-60:00 running order.
- Pre-show commands, variables and bookmarks.
- Complete spoken delivery for each slide.
- Exact terminal commands and screen actions during each demo.
- What to say while a request runs, when it succeeds, when it differs, and when
  switching to recorded evidence.
- The precise sentence for leaving and returning to each demo.
- Scripted answers for the five hidden Q&A slides.

## Essential operating rules

Use the unique `$sessionDir` created in the pre-show setup so a new performance
does not overwrite rehearsal evidence or an earlier approved case.

Give each live request about 30 seconds on stage, and the final focused
evaluation up to 45 seconds. If it is still running, use the labelled recorded
path. Do not retry repeatedly or paste commands into a busy terminal.

Do not run a deployment, install packages, change IAM, or launch a full native
evaluation batch during the presentation. Those are preparation tasks.

The prepared baseline is deliberately defective. The seven-of-nine versus
nine-of-nine results are synthetic-case rehearsal evidence, not a population
accuracy claim. A focused one-case PASS is not a full release approval.

Preview features, data-residency boundaries, and the demo-client release pointer
are explained in the spoken script rather than hidden in technical footnotes.

## Keep the timing

At minute 43, start the final focused recheck even if earlier material ran long.
At minute 47, return to the takeaways. At minute 50, start Q&A.

If five minutes late, use completed scorecards and workflow records, but preserve
the observation -> reviewed expectation -> new test -> corrected-candidate
story. Do not replace it with an extra feature tour.

For resource access, cost, data and fallback preparation, use
[REHEARSAL.md](REHEARSAL.md). For exact deployed versions and live links, use
[DELIVERY.md](DELIVERY.md).
