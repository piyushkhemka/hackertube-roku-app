# HackerTube for Roku

Derived from https://github.com/iBicha/playlet at
`5b204f209534a95e2283ff36c63b6c166d02ec68` (0.48.10).
Original LICENSE (AGPL-3.0) retained. This subtree and modifications are AGPL-3.0.

HackerTube modifications: native paginated catalog grid, local search, area and
category filters, sorting, HackerTube loading/header/home-screen branding, and
a catalog-wide playback allowlist. The working Playlet transport engine remains
unchanged. Account loading, autoplay, SponsorBlock, and upstream diagnostic uploads
are disabled. Only the bundled library loads; the local-only HTTP server exposes
DASH/HLS routes and casting/discovery services are not started.

Playback uses YouTube and Playlet's existing hosted support service.
No availability guarantee or endorsement is implied.

Catalog: 6,454 videos from the 2026-10-31 HackerTube export.
Data attribution: HackerTube and open-index/hacker-news, ODC-By-1.0.
Source: https://hackertube.org/download/hackertube-data.zip
Data license: https://opendatacommons.org/licenses/by/1-0/
