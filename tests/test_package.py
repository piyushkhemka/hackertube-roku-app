import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile
from tools.package import build


class PackageTests(unittest.TestCase):
    def test_reproducible_root_manifest_and_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            a, b = Path(directory) / "a.zip", Path(directory) / "b.zip"
            url = "http://192.0.2.1:8080/diagnostic.mp4"
            self.assertEqual(build(a, url), build(b, url))
            self.assertEqual(a.read_bytes(), b.read_bytes())
            with ZipFile(a) as archive:
                self.assertIn("manifest", archive.namelist())
                self.assertIn("sample_url=" + url, archive.read("manifest").decode())
                self.assertNotIn("data/hackertube-data.zip", archive.namelist())

    def test_manifest_injection_and_credentials_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            for url in ["file:///tmp/a", "https://host/\ntitle=oops", "https://user:secret@host/a"]:
                with self.assertRaises(ValueError):
                    build(Path(directory) / "bad.zip", url)
