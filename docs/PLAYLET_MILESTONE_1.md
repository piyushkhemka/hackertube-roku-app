# HackerTube real-video playback milestone 1

Built 2026-11-07. The owner subsequently confirmed real-video playback and
working play/pause, fast-forward and rewind. The newer catalog app is documented
in [catalog build 2](CATALOG_BUILD_2.md); this file records the earlier milestone.

## Install and test

Sideload `dist/hackertube-roku-playback-milestone-1.zip` using the same Roku
developer installer used for the earlier prototype. The archive contains its
manifest at the root. This replaces the installed diagnostic app in the
developer slot; the earlier build-5 ZIP remains available locally.

Launch **HackerTube** from the Roku home screen. It retains the H tile icon.
The selection screen offers these entries from the HackerTube data export:

1. **Vectors | Chapter 1, Essence of linear algebra** — 3Blue1Brown,
   YouTube ID `fNk_zzaMoSs`.
2. **Ruby Conf 12 - Y Not- Adventures in Functional Programming by Jim Weirich**
   — Confreaks, YouTube ID `FITJMJjASUs`.

Choose the first video with OK. Check picture and audio first, then Play/Pause,
OK, seeking and Back. The upstream player has layered Back handling: it can
first cancel seeking or dismiss controls, then exit playback. This milestone
preserves that behavior rather than modifying controls before playback is proven.
On return, try replaying the first video and then the longer second video.

If loading fails, record the exact on-screen error and which video was selected.
An app-launch error and a stream-resolution error require different fixes.
The Roku developer console on port 8085 can provide additional logs if needed;
logs may contain temporary stream URLs, so avoid publishing them indiscriminately.

Internet is required. The Mac does **not** need to run the diagnostic media server.
Playback uses YouTube and Playlet's existing hosted helper. No official YouTube
app handoff, Google sign-in, or API key is required by this prototype's UI.
Backend availability and playback on this particular device remain unverified.

## Scope

This is a two-video proof of playback, not the full catalog app. The player is
derived from Playlet commit `5b204f209534a95e2283ff36c63b6c166d02ec68`.
The app loads only the embedded pinned library. A job-level allowlist rejects
other video IDs before resolving streams. Autoplay, SponsorBlock and upstream
diagnostic uploads are disabled even if old preferences survived sideloading.
Only loopback DASH/HLS routes are registered; phone casting and DIAL are not started.
Upstream player UI can still contain features outside the milestone, but it
cannot resolve videos outside the sample allowlist.

The existing MIT diagnostic app remains in `roku/`. The derivative source lives
separately in `vendor/playlet/` under its retained AGPL-3.0 license, with attribution
in `HACKERTUBE_UPSTREAM.md`. Exact corresponding source is packaged separately as
`dist/hackertube-roku-playback-milestone-1-source.zip`.

## Build and validation

With Node 22, npm and Python 3 installed:

```sh
bash tools/build_playlet_milestone.sh
```

The script uses the pinned dependency lockfile and disables npm install scripts.
It invokes BrighterScript directly, avoiding upstream signing/deployment hooks.
It packages the embedded library and app, validates assets/XML/ZIP structure,
and writes SHA-256 sidecars for the sideload ZIP and source ZIP.

Checks completed:

- BrighterScript compile/lint and required compiler plugins: app and library
  passed without warnings or errors.
- ZIP CRCs, root manifest, embedded library, manifest asset references and
  packaged XML parsing: passed.
- Source review of bootstrap, home-screen initialization, forced preferences,
  stream-resolution allowlist and local server restrictions: completed.
- Playlet helper `/v1/sts`: HTTP 200 from the development Mac on 2026-11-07.
  This does not verify `/v2/decipher`, YouTube stream delivery or Roku playback.
- Roku runtime tests: **not run**. No device address or developer credentials
  were supplied for this milestone. Upstream tests that deploy to Roku were not run.

Build logs are `dist/playlet-lib-build.log` and `dist/playlet-app-build.log`.
The GitHub build-5 checkpoint has not been changed or replaced.
