# Attribution

Catalog source: [HackerTube](https://hackertube.org/about),
[official export](https://hackertube.org/data), derived from
[open-index/hacker-news](https://huggingface.co/datasets/open-index/hacker-news).
Data is offered under [ODC-By 1.0](https://opendatacommons.org/licenses/by/1-0/).
HN comments remain the work of their authors. Source labels and summaries may
contain errors. The downloaded archive is excluded from source and app packages.

YouTube is the hosting platform for catalog videos; no affiliation is claimed.
No YouTube audiovisual content or thumbnails are bundled. The diagnostic pattern
and tone are generated locally from ffmpeg sources and contain no third-party
footage; project authors release their contribution under the independent prototype's MIT license (see LICENSES/MIT.txt).

## Home-screen icon

The white H / orange rounded-square mark in `assets/hackertube-icon.svg`
is transcribed from the inline SVG favicon served by https://hackertube.org/
on 2026-11-07, at the owner's request. Roku PNG tiles preserve that mark on a
dark background. The source mark remains HackerTube branding; the repository's code
licenses does not imply ownership or a separate trademark license for it.
`assets/roku-tile.html` is the local rendering source (336×210 HD, 248×140 SD).

## Playlet playback foundation

The catalog app is derived from [Playlet](https://github.com/iBicha/playlet),
created by [iBicha](https://github.com/iBicha) and its contributors, at upstream
commit `5b204f209534a95e2283ff36c63b6c166d02ec68` (v0.48.10).
The source and upstream notices remain in `vendor/playlet/` under AGPL-3.0.
HackerTube Roku contributors modified branding, startup, catalog browsing,
filtering, sorting, navigation, and catalog-only playback selection in November
2026. The project is independent of Playlet, YouTube, Roku, and HackerTube.
See [LICENSING.md](LICENSING.md) for the complete license scope.

HackerTube credits [Andrej Karpathy](https://github.com/karpathy) with prompting
its creation; see its [About page](https://hackertube.org/about).
