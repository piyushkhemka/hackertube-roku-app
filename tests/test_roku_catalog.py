import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('prepare_roku_catalog', ROOT / 'tools/prepare_roku_catalog.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CatalogPreparationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = json.loads((ROOT / 'roku/catalog/index.json').read_text())
        cls.taxonomy = json.loads((ROOT / 'roku/catalog/taxonomy.json').read_text())

    def test_every_export_video_is_allowed_and_sorted_once(self):
        catalog, allowed = module.prepare(self.index, self.taxonomy)
        self.assertEqual(set(allowed), {v['id'] for v in self.index})
        self.assertEqual(len(catalog['videos']), 6454)
        for order in catalog['orders'].values():
            self.assertEqual(sorted(order), list(range(6454)))

    def test_taxonomy_membership_matches_export(self):
        catalog, _ = module.prepare(self.index, self.taxonomy)
        category_areas = {c['id']: a['id'] for a in self.taxonomy['areas'] for c in a['categories']}
        for video in catalog['videos']:
            self.assertEqual(set(video['areas']), {category_areas[c] for c in video['categories']})

    def test_duplicates_and_unknown_categories_are_rejected(self):
        with self.assertRaises(ValueError):
            module.prepare([self.index[0], self.index[0]], self.taxonomy)
        bad = dict(self.index[0], categories=['not-a-category'])
        with self.assertRaises(ValueError):
            module.prepare([bad], self.taxonomy)

    def test_empty_catalog_rejected(self):
        with self.assertRaises(ValueError):
            module.prepare([], self.taxonomy)


if __name__ == '__main__':
    unittest.main()
