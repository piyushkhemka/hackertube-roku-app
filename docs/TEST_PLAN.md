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
7. Build 5: verify the native seek bar appears, Left/Rewind seek backward, and
   Right/Fast-forward seek forward. Verify OK and Play/Pause both pause/resume,
   and Back exits the video. Hardware behavior cannot be established by mocks.

M1+ acceptance (pending playback decision): unique record completeness, preserved
source order, zero-recommender/news inclusion, all taxonomy references, last-page
reachability, remote focus restoration, search over title/channel/summary/topics,
registry restart behavior and honest external-handoff/watch-history semantics.

Release is no-go until physical installation and documentation are verified.

Latest local bug review and fixes: [BUG_REVIEW.md](BUG_REVIEW.md). The suite now
contains 9 package tests. The owner has confirmed installation, launch and the 12-second moving test
pattern, Play/Pause and Back on their Roku TV (2026-11-07).
The owner confirmed build 3 OK-button pause/resume and reported seeking was
broken after the focus change. Build 4 adds explicit seek handling and awaits
retesting on hardware. Audio, focus restoration,
error recovery and exact device model/OS remain unverified. This is owner-reported
evidence, not a test directly observed by the agent. Development remains scoped
to the prototype at the owner’s request.


Build 4 local verification: 14 Python tests cover packaging and the range-aware
media server. The BrightScript fixture `tests/playback_controls.brs` was executed
with the external @rokucommunity/brs 0.47.6 interpreter using mocked Video fields.
It failed on build 3's unhandled Right key, then passed with build 4. It covers
seek direction/bounds, paused seek, buffering, key release, OK, Play/Pause and Back.
The interpreter is not a project dependency or part of CI: its legacy dependency
tree has audit findings. The normal compiler and Python checks require no new
packages. This mocked test does not prove actual Roku seeking or Video state behavior.

Build 4 hardware result: the owner reported black-screen flashes on seeking and
preferred the first native-player build. Build 5 restores `m.player.SetFocus(true)`
and removes all custom seek commands. The scene only handles OK/Play when the
native Video node leaves them unhandled, plus Back to exit. This restores the
original key routing with the narrow OK fallback that should have been tried first.

The updated mock fixture checks pause/resume, Back/focus restoration and that
scene code leaves seeking to Video. It cannot verify which keys Video consumes
or whether native controls display correctly. Build 5 requires owner retesting.
