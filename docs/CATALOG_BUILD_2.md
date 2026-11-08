# HackerTube catalog app — build 2

## Install

Sideload `dist/hackertube-roku-catalog-build-2.zip` using the Roku developer
installer. The ZIP has `manifest` at its root and includes the player library.
Open **HackerTube** from the Roku home screen. No Mac server or account is needed.

The previous working two-video ZIP remains at
`dist/hackertube-roku-playback-milestone-1.zip` if a rollback is needed.

## Browse

- The toolbar offers Search, Topics, Sort, Previous, Next and About.
- Press Down to enter the thumbnail grid. OK plays the highlighted video.
- Back from the grid returns to the toolbar. Options (*) opens search.
- Topics contains 16 areas, with a second list for an area or one of its categories.
- Search matches title, channel, topic, summary, tags and category names. Multiple
  words must all match. It combines with the selected topic filter.
- Sort by recommendation score, most recent HN recommendation year, or title.
  Recent means recent recommendations, not YouTube upload date.
- Each page contains at most 24 videos. Previous/Next moves through all results.
- Back from playback uses the existing player behavior: dismiss seeking/controls
  as necessary, then return to the same grid and selection.

## Catalog and playback

All **6,454 videos** in HackerTube's **2026-10-31 export** are bundled, covering
16 areas and 150 categories. This is a snapshot, not automatic synchronization
with future website updates. The export URL and checksum are recorded in
`vendor/playlet/playlet-lib/src/config/hackertube-data-info.json`.

The owner confirmed real-video playback and working transport controls in the
previous milestone on 2026-11-07. This build retains that player implementation.
The stream-resolution gate now accepts exactly the bundled catalog IDs.
Unavailable, removed, restricted or backend-incompatible videos may still fail;
the existing player error/retry UI reports playback failures.

This app does not load account credentials or offer a sign-in interface. General
YouTube search, remote casting/configuration endpoints and automatic playback of
related YouTube videos are not enabled. Playback continues to depend on YouTube
and Playlet's hosted support service.

## Branding and licensing

The Roku home tile, loading screen and catalog header use HackerTube's H icon
and name. The old Playlet splash images are no longer referenced by the manifest,
and its sidebar is hidden. About retains the Playlet AGPL-3.0 attribution and
HackerTube/open-index data attribution (ODC-By-1.0).

The derivative remains in `vendor/playlet/`; the original MIT diagnostic app in
`roku/` is separate. Exact corresponding source is packaged in
`dist/hackertube-roku-catalog-build-2-source.zip`.

## Build and checks

Requirements: Node 22, npm and Python 3.

```sh
# Only needed after updating the normalized export in roku/catalog/:
python3 tools/prepare_roku_catalog.py

# Compile, package, validate, and emit app/source ZIPs and checksums:
bash tools/build_catalog_app.sh

python3 -m unittest discover -s tests -v
```

The corresponding-source ZIP includes the generated bundled catalog, so its
build does not require downloading or regenerating the export.

Validation completed:

- BrighterScript compilation, lint and required plugins: app and library passed
  with no warnings or errors.
- 18 Python tests passed, including catalog membership, taxonomy integrity,
  complete sort permutations, duplicates, empty input and invalid categories.
- Actual compiled catalog filter/pagination logic passed off-device BrightScript
  tests using `@rokucommunity/brs` 0.47.6. Fixtures cover case-insensitive multiword
  search, combined filters, empty results, invalid page/sort handling and serials.
  The full export test confirms 6,454 results over 269 pages, the last 22 entries,
  and the known working 3Blue1Brown video in search results.
- ZIP CRCs, root manifest, icon references, packaged XML, embedded player library,
  catalog/allowlist equality and sorting permutations passed validation.
- The VideoPlayerDev source tree is byte-for-byte unchanged from the player
  version used by the working milestone.

The interpreter tests do not emulate Roku's grid, focus engine, keyboard, images
or hardware decoder. **The new catalog UI and branding still need a TV test.**
Check startup, grid navigation, search, filtering, page changes, and return to
the same selection after a video. No new hardware results are claimed here.
