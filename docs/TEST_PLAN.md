# Validation

Local checks completed: BrighterScript parse/type validation; package byte
reproducibility, root manifest, URL configuration, rejected manifest injection
and credentials; generated media inspection (12 s, H.264 Main, 1280×720, AAC LC).
These checks do not execute SceneGraph or confirm installation.

On real hardware record model, OS and date, then test:

1. Default ZIP launches and explains missing sample configuration on OK.
2. Configured ZIP displays the original pattern and audible tone.
3. Play/Pause pauses and resumes, Back stops, focus returns, retry works.
4. Let the clip finish and verify focus returns to the diagnostic button.
5. Shut down the server and retry; confirm error message and retry recovery.
6. Back from the menu exits normally; Roku Home exits at any point.
7. Record whether native seek controls work; no custom seeking is implemented.

M1+ acceptance (pending playback decision): unique record completeness, preserved
source order, zero-recommender/news inclusion, all taxonomy references, last-page
reachability, remote focus restoration, search over title/channel/summary/topics,
registry restart behavior and honest external-handoff/watch-history semantics.

Release is no-go until physical installation and documentation are verified.

Latest local bug review and fixes: [BUG_REVIEW.md](BUG_REVIEW.md). The suite now
contains 9 package tests. The owner has confirmed installation, launch and the 12-second moving test
pattern, Play/Pause and Back on their Roku TV (2026-11-07).
Build 3 adds OK-button pause/resume and awaits a device retest. Audio, focus restoration,
error recovery and exact device model/OS remain unverified. This is owner-reported
evidence, not a test directly observed by the agent. Development remains scoped
to the prototype at the owner’s request.
