# License scope

The distributed HackerTube Roku catalog app is a modified Playlet derivative,
licensed under GNU AGPL-3.0. The full license is in [LICENSE](LICENSE), and
upstream copyright and license notices remain in [vendor/playlet](vendor/playlet/).
The root license does not replace third-party notices or the exceptions below.

- **Catalog app and its build integration:** AGPL-3.0. This includes our changes
  to `vendor/playlet/`, `tools/build_catalog_app.sh`, and catalog-app tests.
- **Independent original diagnostic prototype:** the original code in `roku/`
  (excluding catalog data and branding), `tools/package.py`,
  `tools/make_diagnostic.sh`, `tools/serve_diagnostic.py`, and their diagnostic
  tests retain the [MIT license and original copyright notice](LICENSES/MIT.txt).
  Previously MIT-licensed independent contributions retain that grant; this
  change does not revoke licenses on earlier versions.
- **Catalog data:** the bundled `roku/catalog/` data and generated
  `vendor/playlet/playlet-lib/src/config/hackertube-*.json` catalog/taxonomy files
  carry ODC-By 1.0 attribution requirements. See [ATTRIBUTION.md](ATTRIBUTION.md).
- **Branding and videos:** HackerTube branding and underlying YouTube videos
  are not relicensed by this repository's code licenses.
- **Other dependencies:** retain their respective licenses and notices.

Each binary release includes a matching source archive with the derivative,
license notices, build scripts, and locked dependency manifests. Build tools
fetch dependencies using the included lockfiles. See the README for rebuilding.
The AGPL license text governs use and redistribution of the derivative.
