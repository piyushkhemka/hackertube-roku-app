# YouTube playback investigation — 2026-11-07

**Follow-up:** The owner subsequently requested Playlet's unofficial approach.
The [Playlet source investigation](PLAYLET_INVESTIGATION.md) establishes a concrete
native playback architecture and supersedes the broad project no-go below for
that revised scope. The findings below still describe the official API question.

## Decision

**No-go for continuing the full native Roku app under the current requirements.**
No documented, supported integration was established for playing arbitrary
HackerTube YouTube selections inside this independent BrightScript/SceneGraph
app. This is an evidence-limited engineering decision, not proof that private
vendor arrangements cannot exist.

The required experience is: browse HackerTube with the Roku remote, select a
video, watch it on the TV, and return to the catalog without a phone or manual
app switching. A catalog with nonfunctional playback does not meet that bar.

## Findings

| Route | Evidence and outcome |
| --- | --- |
| YouTube IFrame player | Official API embeds a player in a website using JavaScript and requires browser HTML5 postMessage. It is not an MP4/HLS media URL for the existing SceneGraph Video node. No supported browser embedding component for this project was established. |
| YouTube Data API | The video resource provides metadata and player embed HTML. Its fileDetails video/audio streams are metadata about the uploaded file, restricted to the owner, not playback URLs. Adding an API key does not resolve playback. |
| Cobalt TV runtime | A real Google platform for HTML5 TV applications. Porting requires a native toolchain and platform implementations for OS, graphics, input, media, DRM and other functions. This is platform integration work, not a documented BrightScript player library. No public route to deploy that runtime in our sideloaded Roku package was established. |
| Private/device partnership | Google directs YouTube-specific Cobalt questions to a YouTube technical account manager. This suggests a vendor discussion is relevant, but does not establish our eligibility, access, pricing, or permission to embed YouTube in a third-party Roku catalog. |
| Launch official YouTube app | A potential separate-app design, not embedded playback. No supported YouTube-specific contract for selecting a video from this Roku app and returning to its catalog was verified. Roku ECP and deep-link documentation were inaccessible here. Do not treat guessed channel IDs, URL parameters, or external-controller commands as a supported in-app integration. |
| Phone casting / TV code | Google documents this workflow using its YouTube apps. It adds a phone and separate app flow, which the owner has rejected as the core product experience. |
| Extracted streams / proxy | Not accepted as an authorized integration. YouTube API policies restrict audiovisual access through other technology and downloading/caching without prior written approval. These techniques were not implemented or tested. |

## Primary sources

Read through gstack browse on 2026-11-07:

- [IFrame Player API](https://developers.google.com/youtube/iframe_api_reference): website JavaScript player and browser requirements.
- [Video resource](https://developers.google.com/youtube/data/reference/rest/v3/videos): embedHtml and fileDetails schema.
- [Cobalt overview](https://developers.google.com/youtube/cobalt): HTML5 TV application platform.
- [Porting Cobalt](https://developers.google.com/youtube/cobalt/docs/starboard/porting): native platform port requirements. Conclusion about its mismatch with our SceneGraph package is an engineering inference from these requirements; this source does not explicitly prohibit a Roku port.
- [Cobalt communication](https://developers.google.com/youtube/cobalt/docs/communication): YouTube-specific questions go to a YouTube technical account manager; Cobalt maintainers do not speak for YouTube.
- [YouTube developer policies](https://developers.google.com/youtube/terms/developer-policies): audiovisual access, player integrity, advertisements and approval requirements.
- [Official TV casting instructions](https://support.google.com/youtube/answer/7640706?hl=en): phone/app casting and TV-code workflow.

Attempted official Roku sources, all returning CloudFront HTTP 403:

- [Video node](https://developer.roku.com/docs/references/scenegraph/media-playback-nodes/video.md)
- [External Control API](https://developer.roku.com/docs/developer-program/debugging/external-control-api.md)
- [Deep linking](https://developer.roku.com/docs/developer-program/discovery/implementing-deep-linking.md)

Consequently, this investigation does not assert a currently verified Roku
certification ban, ECP launch permission, or YouTube-specific launch parameters.
No Roku device launch experiment or real YouTube playback test was performed.

## What would reopen the project

Obtain a documented integration and authorization from the relevant vendors,
then prove one actual catalog video on the owner's Roku before resuming UI work.
The following inquiry is prepared but **has not been sent**:

> We are developing an independent BrightScript/SceneGraph Roku app that browses
> a curated catalog of third-party YouTube videos. We require remote-only video
> selection, playback on the same TV, and return to the catalog. Is there a
> supported YouTube player SDK/runtime available to independent Roku developers?
> If so, please provide its documentation, access requirements, permissions for
> third-party videos, ad/account/restriction handling, and sideload versus public
> distribution eligibility. If embedding is unavailable, is there an officially
> supported in-channel launch contract for the Roku YouTube app, including
> video selection and return navigation? Please distinguish this from external
> LAN-controller APIs and phone casting.

Google's policy page links its [API inquiry/approval form](https://support.google.com/youtube/contact/yt_api_form).
This is an inquiry route, not evidence that a Roku SDK or exception is available.
Existing device partners can use their YouTube technical account manager.
Roku developer support must separately confirm runtime and launch capabilities.

Acceptance test for any proposed route: play an actual HackerTube selection,
verify audio, OK/Play-Pause, seeking and Back-to-catalog on hardware, and verify
documented handling for unavailable/restricted videos and required YouTube UI.

## Project impact

The diagnostic clip demonstrated ordinary MP4 playback and remote behavior;
it did not validate YouTube access. More diagnostic clip work cannot resolve
this integration gap.

No application functionality was changed during this investigation. The build-5
GitHub checkpoint remains the last checkpoint. Earlier untracked catalog import
and Task/logic work remains local, incomplete and unvalidated; it is not a
finished app or a new release. No new ZIP or GitHub checkpoint was created.
