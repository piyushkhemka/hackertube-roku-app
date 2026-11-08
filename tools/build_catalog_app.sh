#!/usr/bin/env bash
set -euo pipefail
project_dir="$(cd "$(dirname "$0")/.." && pwd)"
playlet_dir="$project_dir/vendor/playlet"
if [[ "$(node -p 'process.versions.node.split(".")[0]')" != 22 ]]; then
    echo 'This pinned Playlet build requires Node 22 on PATH.' >&2
    exit 1
fi
mkdir -p "$project_dir/dist"
if [[ ! -x "$playlet_dir/node_modules/.bin/bsc" ]]; then
    (cd "$playlet_dir" && npm ci --ignore-scripts --no-audit --no-fund)
fi
export npm_lifecycle_event=build:catalog
# Invoke the compiler directly: upstream production hooks require Roku signing.
for component in playlet-lib playlet-app; do
    (
        cd "$playlet_dir/$component"
        ../node_modules/.bin/bsc --create-package --sourceMap=false --lintConfig ../config/bslint.jsonc
    ) > "$project_dir/dist/$component-build.log" 2>&1 || {
        cat "$project_dir/dist/$component-build.log" >&2
        exit 1
    }
    if [[ "$component" == playlet-lib ]]; then
        mkdir -p "$playlet_dir/playlet-app/src/lib"
        cp "$playlet_dir/dist/playlet-lib.zip" "$playlet_dir/playlet-app/src/lib/playlet-lib.zip"
    fi
done
python3 - "$project_dir" <<'PY'
import hashlib
import io
import json
from pathlib import Path
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET

root = Path(sys.argv[1])
vendor = root / 'vendor/playlet'
artifact = root / 'dist/hackertube-roku-catalog-build-2.zip'
shutil.copyfile(vendor / 'dist/playlet-app.zip', artifact)
with zipfile.ZipFile(artifact) as app:
    assert app.testzip() is None, 'App ZIP CRC failure'
    manifest = dict(line.split('=', 1) for line in app.read('manifest').decode().splitlines()
                    if '=' in line and not line.startswith('#'))
    assert manifest['title'] == 'HackerTube'
    assert manifest['playlet_lib_zip_embedded_url'] == 'pkg:/lib/playlet-lib.zip'
    assert not any('remote_url' in key for key in manifest)
    for key, value in manifest.items():
        if value.startswith('pkg:/'):
            assert value[5:] in app.namelist(), (key, value)
    assert 'config/HACKERTUBE_LICENSE.txt' in app.namelist()
    with zipfile.ZipFile(io.BytesIO(app.read('lib/playlet-lib.zip'))) as lib:
        assert lib.testzip() is None, 'Library ZIP CRC failure'
        catalog = json.loads(lib.read('config/hackertube-catalog.json'))
        allowed = json.loads(lib.read('config/hackertube-allowed.json'))
        info = json.loads(lib.read('config/hackertube-data-info.json'))
        ids = [v['id'] for v in catalog['videos']]
        assert len(ids) == len(set(ids)) == info['count']
        assert set(ids) == set(allowed), 'Playback allowlist differs from catalog'
        for order in catalog['orders'].values():
            assert sorted(order) == list(range(len(ids)))
        assert 'splash_screen_hd' not in manifest
        assert 'images/hackertube-hd.png' in lib.namelist()
        assert lib.read('components/Screens/HomeScreen/HomeScreen.brs')
        assert lib.read('components/VideoPlayer/VideoContentJob.brs')
        for name in lib.namelist():
            if name.endswith('.xml'):
                ET.fromstring(lib.read(name))
    for name in app.namelist():
        assert not name.startswith('/') and '..' not in Path(name).parts
        if name.endswith('.xml'):
            ET.fromstring(app.read(name))

# Supply the exact corresponding derivative source, without dependencies/build output.
source = root / 'dist/hackertube-roku-catalog-build-2-source.zip'
excluded = {'.git', 'node_modules', 'build', 'dist', 'release', '__pycache__'}
with zipfile.ZipFile(source, 'w', zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(vendor.rglob('*')):
        rel = path.relative_to(vendor)
        if not path.is_file() or path.is_symlink() or excluded.intersection(rel.parts):
            continue
        if rel.as_posix() == 'playlet-app/src/lib/playlet-lib.zip' or path.name == '.DS_Store':
            continue
        archive.write(path, 'vendor/playlet/' + rel.as_posix())
    archive.write(root / 'tools/build_catalog_app.sh', 'tools/build_catalog_app.sh')
for path in (artifact, source):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    path.with_suffix('.zip.sha256').write_text(f'{digest}  {path.name}\n')
    print(f'{path}\nSHA-256: {digest}')
print('Validated root manifest, embedded library, asset references, XML and ZIP CRCs.')
PY
