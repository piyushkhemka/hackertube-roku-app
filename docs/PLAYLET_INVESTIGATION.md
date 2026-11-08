# Playlet investigation — 2026-11-07

## Revised feasibility decision

Playlet provides a concrete architecture for unofficial native YouTube playback
on Roku. The earlier no-go decision was limited to officially supported YouTube
interfaces; it was too restrictive for the owner's newly stated goal of adapting
Playlet for personal HackerTube use. Proceeding with a Playlet-based playback
prototype is technically justified. Actual playback on this user's Roku is still
unverified; source inspection is not a successful hardware test.

Reviewed repository: https://github.com/iBicha/playlet

Pinned source: `5b204f209534a95e2283ff36c63b6c166d02ec68`, package version `0.48.10`.
This is the checked-out default-branch source, not a claim that every feature is
in the installed store release. Local inspection checkout is at
`/tmp/hackertube-playlet-investigation`.

## Actual playback path

1. A catalog item supplies a YouTube `videoId`.
2. `VideoPlayerDev.PlayWithContent` queues `VideoContentJob`.
3. That job selects either the default Playlet/InnerTube backend or Invidious.
4. InnerTube calls YouTube's internal player endpoint and parses stream metadata.
   It also calls Playlet's hosted helper for signature timestamp and URL
   deciphering. Invidious instead supplies video metadata and resolved URLs from
   its configured server.
5. The job chooses adaptive DASH, muxed streams, or HLS as appropriate. For DASH
   it builds a localhost URL served by Playlet's HTTP server running on the Roku.
   `DashRouter` and `DashManifest` generate a manifest using the stream metadata,
   with codec/quality handling. This is not necessarily a full media relay:
   manifest generation and optional video proxying are distinct functions.
6. The resulting URL becomes the content URL of a native SceneGraph `Video`
   component. Roku decodes the media, while Playlet supplies controls and UI.

The selected player at this commit is **VideoPlayerDev** (`USE_DEV_PLAYER=true`
in `VideoQueue.bs`). Both it and the older VideoPlayer extend native Video.
The newer player disables OS chrome and implements its own transport controls;
copying only the old player would miss the currently selected implementation.

This architecture does not embed a YouTube webpage or launch official YouTube.
The companion Svelte web app is optional remote UI, not the Roku's player engine.

## Source map

Paths below are relative to the pinned [source tree](https://github.com/iBicha/playlet/tree/5b204f209534a95e2283ff36c63b6c166d02ec68).

| Responsibility | Source |
| --- | --- |
| Default backend | `playlet-lib/src/config/preferences.json5` |
| Active player selection | `playlet-lib/src/components/VideoQueue/VideoQueue.bs` |
| Native player and controls | `playlet-lib/src/components/VideoPlayerDev/VideoPlayerDev.xml`, `.bs`, and `README.md` |
| Resolve selected video and assign URL | `playlet-lib/src/components/VideoPlayer/VideoContentJob.bs` |
| Internal YouTube requests and response parsing | `playlet-lib/src/components/Services/Innertube/PlayerEndpoint.bs`, `InnertubeService.bs` |
| Hosted helper location | `playlet-lib/src/components/Services/Innertube/Constants.bs` |
| Optional Invidious API | `playlet-lib/src/components/Services/Invidious/InvidiousService.bs` |
| Local manifest endpoint | `playlet-lib/src/components/Web/PlayletWebServer/Middleware/DashRouter.bs` |
| DASH generation and codec selection | `playlet-lib/src/components/Services/Dash/DashManifest.bs` |
| Packaging/component library | `docs/README.md`, `playlet-app/package.json` |

## Dependencies and practical limits

- The default backend is labeled local, but is not self-contained. It references
  a hosted DigitalOcean helper through `PLAYLET_SUPPORT_SERVER`, using `/v1/sts`
  and `/v2/decipher`. No implementation of those helper endpoints was located in
  the inspected repository. Do not assume cloning the app supplies that service
  or that its operator guarantees support for another app.
- Invidious is optional, not the sole current playback backend. A separate
  always-on Mac server is not intrinsically required by the default architecture;
  a self-hosted backend would create its own availability requirement.
- Source includes session/token handling, retries, format selection, live-video
  handling and codec filtering. This is substantially more than passing a
  YouTube watch URL to Video. Upstream changes can break it.
- The maintainer's [2026 update](https://github.com/iBicha/playlet/discussions/827)
  describes the playback maintenance burden and hosted URL-decipher service.
  The announcement also discusses future work; the pinned source determines
  what was actually present in this inspection.
- Playlet identifies itself as unofficial. Technical viability does not establish
  YouTube approval or guaranteed Roku store eligibility for a derivative.
- The repository is AGPL-3.0 licensed. A derivative must retain its license and
  attribution and account for its source-availability requirements; it cannot be
  treated as MIT code simply because our diagnostic prototype is MIT.

## Recommended HackerTube implementation

Use a separately pinned Playlet-based derivative rather than extracting a few
player files into the diagnostic prototype. Its player relies on job queues,
HTTP server, services, profiles, preferences and generated component bindings.
Retaining these initially reduces integration risk and makes upstream fixes
easier to incorporate.

1. Establish a reproducible sideload build of pinned upstream source. Audit build
   hooks: production scripts include signing and tests include device deployment;
   do not run them blindly or assume device credentials exist.
2. Add a minimal HackerTube selection screen with a small sample from the actual
   catalog. Preserve the H icon and HackerTube identity with Playlet attribution.
3. Verify real catalog video playback, audio, seeking, OK/Play-Pause and Back on
   the TV before expanding UI. Test short and long videos, replay after URL
   expiry, and unavailable-video behavior. No diagnostic clip substitutes here.
4. Replace home/search/category feeds with HackerTube's data. Enforce catalog
   membership at the playback queue boundary as well as in UI. Disable or filter
   general YouTube search, related videos, autoplay, deep links and remote queue
   requests; otherwise a nominally HackerTube-only UI can still play other videos.
5. Choose and document backend operations: compatibility of the existing helper
   for the prototype, and a maintainable helper or Invidious deployment for an
   independent installation. Do not promise a server-free or maintenance-free app.
6. Keep app/library versions pinned to our build. Upstream's latest-library
   auto-loading must not silently replace the HackerTube adaptation. Disable
   unrelated upstream telemetry for the derivative and preserve useful local
   diagnostics.

## Work performed

Cloned and traced source, checked the maintainer's announcement through gstack,
and revised the feasibility assessment. No packages were installed, no Playlet
backend requests or YouTube streams were fetched, and no Roku playback test was
run. Only documentation in the HackerTube project was changed. Existing local
catalog work and the GitHub build-5 checkpoint are preserved.
