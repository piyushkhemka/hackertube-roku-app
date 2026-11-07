# Playback feasibility — 2026-11-07

**Diagnostic MP4 playback: confirmed by owner on Roku, 2026-11-07.**
**Native arbitrary YouTube playback: BLOCKED; no authorized route verified.**
No documented, authorized mechanism has been established for this independent
BrightScript/SceneGraph app. This is an evidence-limited conclusion, not a claim
that private platform partnerships cannot exist.

## Evidence reviewed

- [YouTube IFrame API](https://developers.google.com/youtube/iframe_api_reference):
  website JavaScript API requiring browser HTML5 postMessage. This is not a
  SceneGraph Video stream interface.
- [YouTube video resource](https://developers.google.com/youtube/data/reference/rest/v3/videos):
  metadata and player embed HTML; no documented general-purpose playback-stream
  URL field suitable for this app.
- [YouTube developer policies](https://developers.google.com/youtube/terms/developer-policies):
  audiovisual access and player integrity restrictions rule out treating
  stream extraction or rehosting as an approved integration.
- [Roku Video reference](https://developer.roku.com/docs/references/scenegraph/media-playback-nodes/video.md)
  and [playing videos](https://developer.roku.com/dev/docs/playing-videos):
  attempted through gstack browser; HTTP 403 from CloudFront. Current format
  compatibility documentation could not be verified from this environment.
- [Official Roku sample repository](https://github.com/rokudev/samples): inspected;
  describes physical-device sideloading and points to its new GitLab home.

## Implemented spike

SceneGraph entry point and Video node, explicit user-started MP4 diagnostic,
state/error logging, pause/resume and Back. A local ffmpeg command generates an
original 12-second test pattern and sine tone. No third-party audiovisual media
is downloaded or included. Serve it on the Mac and configure the LAN URL at build
time. The default ZIP explains configuration instead of attempting a bogus URL.

The owner confirmed playback of the 12-second moving test pattern using
`hackertube-roku-tv-test.zip` and the Mac LAN media server. This establishes
diagnostic MP4 video playback on their device, not YouTube playback or permission
to redistribute catalog videos. The agent did not directly observe the TV.

## Hardware test log

| Item | Result |
| --- | --- |
| Roku model / OS | Owner’s Roku TV; exact model and OS not provided |
| Install / launch | PASS — owner reported sideload and diagnostic screen launch |
| Picture | PASS — owner reported playing the 12-second moving test pattern on 2026-11-07 |
| Audio | Not separately confirmed |
| Play/Pause button | PASS — owner confirmed pause/resume |
| Back button | PASS — owner confirmed Back works |
| OK button | Owner reported no pause/resume in build 2; handler added in build 3, awaiting retest |
| Seek | Not yet reported |
| Missing server / retry | Not yet reported |
| YouTube playback | NOT RUN; no authorized route |

Capture actual values, date, console errors and results here after testing. No
hardware screenshots or performance measurements are available.

## Decision gate

The basic physical-device video test passed by owner report; audio, OK-button retest,
error recovery and device details remain unverified. Full native YouTube
playback is no-go. Proposed alternative: full catalog browser with an explicitly
labeled YouTube URL/QR handoff. The user opens official YouTube on a phone and
uses its supported TV linking/casting when available; this is not an automatic
Roku app launch. No watch history can be inferred from showing the link.

The owner chose to stop after the playback prototype. The proposed fallback is
not approved for implementation. No importer or full UI has been implemented.

## Local validation result

`npm test` passed BrighterScript validation and 9 Python package tests (latest run).
`npm run build` produced the M0 ZIP and SHA-256 file. ffprobe confirmed a 12-second
1280×720 H.264 Main / AAC LC diagnostic clip. The official archive was inspected:
6,454 unique video records, 16 areas and 150 categories; see DATA_INSPECTION.md.
