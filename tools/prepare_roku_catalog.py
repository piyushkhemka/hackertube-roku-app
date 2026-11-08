"""Prepare the compact, offline catalog consumed by the Playlet-derived Roku UI."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'vendor/playlet/playlet-lib/src/config'


def prepare(index, taxonomy):
    categories = {c['id']: area['id'] for area in taxonomy['areas'] for c in area['categories']}
    seen = set()
    videos = []
    for row in index:
        vid = row['id']
        if vid in seen or not re.fullmatch(r'[A-Za-z0-9_-]{11}', vid):
            raise ValueError(f'Duplicate or invalid video ID: {vid}')
        seen.add(vid)
        if any(c not in categories for c in row['categories']):
            raise ValueError(f'Unknown category: {vid}')
        videos.append({k: row[k] for k in ('id', 'title', 'channel', 'categories', 'search', 'score', 'lastYear', 'recommenders')})
        videos[-1]['areas'] = sorted({categories[c] for c in row['categories']})
    if not videos:
        raise ValueError('Empty catalog')
    orders = {
        'recommended': sorted(range(len(videos)), key=lambda n: (-videos[n]['score'], -videos[n]['recommenders'], videos[n]['id'])),
        'recent': sorted(range(len(videos)), key=lambda n: (-videos[n]['lastYear'], -videos[n]['score'], videos[n]['id'])),
        'az': sorted(range(len(videos)), key=lambda n: (videos[n]['title'].casefold(), videos[n]['id'])),
    }
    return {'videos': videos, 'orders': orders}, {vid: True for vid in sorted(seen)}


def main():
    source = ROOT / 'roku/catalog'
    index = json.loads((source / 'index.json').read_text())
    taxonomy = json.loads((source / 'taxonomy.json').read_text())
    manifest = json.loads((source / 'catalog-manifest.json').read_text())
    catalog, allowed = prepare(index, taxonomy)
    if len(allowed) != manifest['count']:
        raise ValueError('Manifest count does not match catalog')
    OUTPUT.mkdir(parents=True, exist_ok=True)
    files = {'hackertube-catalog.json': catalog, 'hackertube-allowed.json': allowed,
             'hackertube-taxonomy.json': taxonomy,
             'hackertube-data-info.json': {k: manifest[k] for k in ('count', 'sourceVersion', 'sourceUrl', 'sourceSha256', 'license', 'attribution')}}
    for name, data in files.items():
        (OUTPUT / name).write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n')
    print(f'Prepared {len(allowed)} catalog videos, {len(taxonomy["areas"])} topic areas.')


if __name__ == '__main__':
    main()
