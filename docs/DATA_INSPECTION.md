# Official export inspection

Downloaded the link discovered on https://hackertube.org/data, then read the
archive's actual `hackertube-data/DATA.md` before designing an importer. A local
copy is at `data/DATA.md`. Numeric results and archive SHA-256 are recorded in
[DATA_INSPECTION.json](DATA_INSPECTION.json).

Verified 6,454 distinct IDs, 39,834 mentions, 3,778 related rows, 16 areas and 150
categories. IDs all match the 11-character YouTube format; category references
and related target IDs resolve. Source score order is nonincreasing.

Clarifications to the brief:

- ZIP members have a `hackertube-data/` prefix, rather than living at archive root.
- Video taxonomy lives in `categories[]` objects; `primary_topic` is free text.
  Taxonomy contains `areas[].categories[]`, with descriptions useful for search.
- Format is `content_type`; no durations, YouTube descriptions or live
  availability status are supplied. Search can use summaries; duration filters
  require optional enrichment and cannot be inferred reliably from content type.
- HN counts are nested under `hn`; 1,658 videos have zero recommenders. There are
  407 news records. Both groups must remain reachable in All Videos.
- `quote` may be null. Recommendation context must distinguish `rec`/`strong_rec`
  from reference, joke and critical mentions. Mentions are capped at 20 per video.
- Related edges are `related[].vid` with `shared_recommenders` counts.
- Source DATA.md suggests hiding news/unavailable videos and optional title
  deduplication. Those suggestions are source documentation, not app requirements:
  the handoff requires preserving all distinct IDs, with honest availability.
- No embeddings need to ship to Roku. There is no exported playable media URL.

No importer has been implemented yet; this is inspection, not completion of M1.
