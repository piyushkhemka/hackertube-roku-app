# Changelog

## 0.0.1 — unreleased

- M0 SceneGraph diagnostic and original generated test media workflow.
- Deterministic sideload ZIP/checksum, compiler checks, package tests and CI.
- Evidence-limited playback feasibility report and actual export schema inspection.
- Full browser and physical Roku validation remain pending.

### Prototype fixes

- Harden URL/manifest validation and exclude hidden files and symlinks.
- Preserve the previous ZIP on build failure; reject output inside source.
- Add explicit menu Back exit handling and expand to 9 package tests.

- Add HackerTube H home-screen tiles, set the display name to HackerTube, and bump Roku build to 2.

- Build 3: OK and Play/Pause both toggle playback; route playback keys to the scene. Owner confirmed Play/Pause and Back on build 2.

- Build 4: restore seeking with five-second Left/Rewind and Right/Fast-forward steps while keeping OK pause/resume. Add a byte-range diagnostic server and HTTP regression tests. Hardware retest pending.

- Build 5: restore native Video focus/seek UI from the first working build; remove five-second jumps. Retain scene-level OK pause/resume fallback and Back exit. Owner reported black-screen flashes and unclear seeking in build 4.
