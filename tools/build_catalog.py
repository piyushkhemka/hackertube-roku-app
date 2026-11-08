"""Deterministically convert the official HackerTube ZIP into a bundled Roku catalog."""
import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = 1
SHARD_SIZE = 100
VID = re.compile(r"[A-Za-z0-9_-]{11}\Z")


def encode(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def load_export(path):
    with ZipFile(path) as archive:
        names = archive.namelist()
        docs = [name for name in names if name == "DATA.md" or name.endswith("/DATA.md")]
        if len(docs) != 1:
            raise ValueError("Expected one DATA.md in official export")
        prefix = docs[0][:-len("DATA.md")]
        documentation = archive.read(docs[0]).decode("utf-8")
        date = re.search(r"Exported (\d{4}-\d{2}-\d{2})", documentation)
        if not date:
            raise ValueError("Source export date missing in DATA.md")
        def rows(name):
            return [json.loads(line) for line in archive.read(prefix + name).splitlines() if line.strip()]
        return (date.group(1), rows("videos.jsonl"),
                json.loads(archive.read(prefix + "taxonomy.json")),
                rows("mentions.jsonl"), rows("related.jsonl"))


def normalize(source):
    version, raw, taxonomy, mentions, related = source
    categories = {}
    areas = set()
    for area in taxonomy["areas"]:
        if area["id"] in areas:
            raise ValueError("Duplicate area")
        areas.add(area["id"])
        for category in area["categories"]:
            if category["id"] in categories:
                raise ValueError("Duplicate category")
            categories[category["id"]] = category
    videos, seen = [], {}
    for row in raw:
        vid = row["vid"]
        if not VID.fullmatch(vid):
            raise ValueError(f"Invalid video ID: {vid!r}")
        if vid in seen:
            if seen[vid] != row:
                raise ValueError(f"Conflicting duplicate: {vid}")
            continue
        if not isinstance(row["title"], str) or not row["title"].strip():
            raise ValueError(f"Missing title: {vid}")
        for category in row["categories"]:
            if category["id"] not in categories or category["area"] not in areas:
                raise ValueError(f"Unknown taxonomy reference: {vid}")
        seen[vid] = row
        videos.append(row)
    if not videos:
        raise ValueError("Empty catalog")
    contexts = defaultdict(list)
    for mention in mentions:
        if mention["vid"] not in seen:
            raise ValueError("Orphan HN mention")
        if mention["stance"] in {"rec", "strong_rec"}:
            contexts[mention["vid"]].append({
                "id": mention["hn_comment_id"], "stance": mention["stance"],
                "quote": mention.get("quote", ""), "story": mention.get("story_title", ""),
                "url": f'https://news.ycombinator.com/item?id={mention["hn_comment_id"]}',
            })
    related_by_id = {}
    for row in related:
        if row["vid"] not in seen or any(r["vid"] not in seen for r in row["related"]):
            raise ValueError("Orphan related-video reference")
        related_by_id[row["vid"]] = [r["vid"] for r in row["related"]]
    index, details = [], []
    for rank, row in enumerate(videos):
        cats = [category["id"] for category in row["categories"]]
        text = " ".join([row["title"], row.get("channel") or "", row.get("summary") or "",
                         row.get("primary_topic") or "", " ".join(row.get("tags", [])),
                         " ".join(categories[c]["name"] for c in cats)]).lower()
        index.append({
            "id": row["vid"], "title": row["title"], "channel": row.get("channel") or "Unknown channel",
            "topic": row.get("primary_topic") or "", "categories": cats,
            "type": row["content_type"], "life": row["shelf_life"], "score": row["score"],
            "recommenders": row["hn"]["recommenders"], "lastYear": row["hn"]["last_year"],
            "search": text, "shard": rank // SHARD_SIZE,
        })
        details.append({**row, "availability": "unknown", "recommendations": contexts[row["vid"]][:3],
                        "related": related_by_id.get(row["vid"], [])})
    return version, taxonomy, index, details, len(raw), len(mentions)


def build(source_zip: Path, output: Path):
    version, taxonomy, index, details, raw_count, mentions_count = normalize(load_export(source_zip))
    assets = {"index.json": encode(index), "taxonomy.json": encode(taxonomy)}
    for start in range(0, len(details), SHARD_SIZE):
        assets[f"details/{start // SHARD_SIZE}.json"] = encode(
            {row["vid"]: row for row in details[start:start + SHARD_SIZE]})
    manifest = {
        "schemaVersion": SCHEMA, "sourceVersion": version, "count": len(index),
        "sourceRows": raw_count, "mentions": mentions_count, "shardSize": SHARD_SIZE,
        "sourceUrl": "https://hackertube.org/download/hackertube-data.zip",
        "sourceSha256": hashlib.sha256(source_zip.read_bytes()).hexdigest(),
        "license": "ODC-By-1.0", "attribution": "HackerTube and open-index/hacker-news",
        "dataVersion": hashlib.sha256(b"".join(assets[n] for n in sorted(assets))).hexdigest(),
        "assets": {name: {"sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
                   for name, data in sorted(assets.items())},
    }
    assets["catalog-manifest.json"] = encode(manifest)
    output.mkdir(parents=True, exist_ok=True)
    for path in output.rglob("*.json"):
        if path.relative_to(output).as_posix() not in assets:
            path.unlink()
    for name, data in assets.items():
        path = output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, default=ROOT / "roku/catalog")
    args = parser.parse_args()
    result = build(args.source, args.output)
    print(f'{result["count"]} videos; source {result["sourceVersion"]}; '
          f'{sum(a["bytes"] for a in result["assets"].values()):,} bundled JSON bytes')
