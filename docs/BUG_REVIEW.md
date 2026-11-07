# Prototype bug review — 2026-11-07

Scope: M0 only. The owner's decision to stop after the playback prototype remains
in effect. No catalog browser or handoff features were added.

## Reproduced and fixed

- URL validation accepted nonnumeric/out-of-range ports, NUL/DEL characters and
  empty userinfo. Invalid configurations now fail before writing a package.
- A manifest with an existing sample URL concatenated the new and old URLs.
  Packaging now replaces the entire value and requires one configuration entry.
- Hidden files and symlinks were copied into the ZIP, including external linked
  content. Both are excluded.
- Output inside `roku/` could package the ZIP being written. Such output is rejected.
- Missing manifests still produced packages; validation now fails before writing.
- A build error could destroy the previous ZIP. A temporary ZIP is now completed
  before replacement. An injected read error verifies preservation and cleanup.

The new regression cases failed against the original code and pass after fixes.

## Lifecycle improvement

Menu Back previously fell through without an explicit application exit handler.
It now signals the main event loop to close the screen. Back during playback
still stops the diagnostic and restores menu focus. Compilation is verified;
actual remote event routing and exit behavior are not hardware-tested.

## Results

- `npm test`: BrighterScript validation and all 9 Python tests pass.
- `npm run build`: success; regenerated diagnostic ZIP and checksum.
- ZIP CRC, root manifest, XML parsing and SHA-256 verification: pass.
- `npm audit --audit-level=moderate`: 0 reported vulnerabilities.
- `sh -n tools/make_diagnostic.sh` and `git diff --check`: pass.

## Still unverified

No Roku device was supplied or used. Installation, video decoding, buffering,
remote pause/resume/Back, focus after completion/errors and retry behavior still
require the physical-device checks in TEST_PLAN.md. Static validation does not
execute SceneGraph. No native YouTube playback is implemented or claimed.
