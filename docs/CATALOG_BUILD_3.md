# Catalog build 3 — scrolling and toolbar focus

Install `dist/hackertube-roku-catalog-build-3.zip` through the Roku developer
installer. Build 2 remains available for rollback.

## Changes

- Search, Topics, Sort and About now use a separate toolbar focus target. OK is
  routed according to the node that actually has focus, and playback rejects
  selection events when the toolbar or picker is active.
- The grid explicitly handles arrow keys and renders eight reusable cards.
  Down scrolls through the loaded rows and fetches the next 24 videos near the
  bottom. New results append; earlier results remain available by pressing Up.
- At a loading boundary, a pending Down advances into the new rows once they
  arrive. Moving away, opening a picker or playing a video cancels that pending
  movement. Failed loads keep existing rows and allow retry with Down.
- Next/Previous controls and page numbers are removed. Back from the grid, or
  Up from its first row, returns to the toolbar.

## Verification

BrighterScript compilation/lint and app/library package validation passed.
Off-device tests of the compiled HomeScreen logic passed for scrolling beyond
the visible rows, appending a second batch, returning to earlier rows, ignoring
stale responses, rejecting playback from the toolbar, and activating Topics
with toolbar OK. The test uses mock focus targets; it does not emulate Roku's
native focus engine or display.

The owner confirmed launch and playback in build 2. This updated navigation
still needs a TV test: press OK on Search/Topics, then scroll Down through more
than 24 videos and back Up. The playback engine itself was not modified.

Build with Node 22: `bash tools/build_catalog_app.sh`.
Exact corresponding source: `dist/hackertube-roku-catalog-build-3-source.zip`.
Navigation test: `tests/catalog_navigation.brs`, run against the compiled
HomeScreen with `@rokucommunity/brs` 0.47.6.
