# Catalog build 4 — topic and sort selection

Install `dist/hackertube-roku-catalog-build-4.zip` through the Roku developer installer.

Topic and sort pickers now explicitly handle Up/Down/OK using a focused Group,
matching the grid navigation, instead of relying on native LabelList selection events.
Choosing a topic applies it immediately; indented subtopics can also be selected.
The current filter/order is highlighted when reopening its menu. Back cancels.
Each applied choice resets pagination and replaces the old results. Sorting retains
the active search and topic. Pending requests now start after any non-running task
state, including completion, so a choice during prefetch is not stranded.

Top recommended uses the bundled HackerTube recommendation-score order (highest
first, with recommender count as a tie-breaker). It is the default order, so choosing
it again while already active will preserve the same order. Recently recommended
uses the latest HN recommendation year, not the YouTube upload date.

Validation: app/library compilation and lint, ZIP/root-manifest/assets/XML validation,
18 Python tests, compiled BrightScript navigation/picker and catalog-filter tests.
The off-device tests use mocked focus nodes. The owner subsequently confirmed
that build 4 works on their Roku, including the topic and sort fixes.
Playback code was not changed.

TV check: choose a topic and confirm the count drops; choose Title A-Z, then Top
recommended and confirm the first videos change; scroll Down past the first batch.

Build with Node 22: `bash tools/build_catalog_app.sh`.
Corresponding source: `dist/hackertube-roku-catalog-build-4-source.zip`.
