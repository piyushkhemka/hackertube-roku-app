import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile
from unittest.mock import patch
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

    def test_invalid_ports_controls_and_empty_credentials_rejected(self):
        urls = ["http://host:bad/a", "http://host:99999/a", "http://host/\x00a",
                "http://@host/a", "http://host/\x7fa"]
        with tempfile.TemporaryDirectory() as directory:
            for url in urls:
                with self.subTest(url=repr(url)), self.assertRaises(ValueError):
                    build(Path(directory) / "bad.zip", url)

    def test_replaces_existing_manifest_value(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "roku").mkdir()
            (root / "roku/manifest").write_text("title=Test\nsample_url=http://old/a\n")
            with patch("tools.package.ROOT", root):
                output = root / "out.zip"
                build(output, "http://new/b")
                with ZipFile(output) as archive:
                    self.assertEqual(archive.read("manifest").decode(),
                                     "title=Test\nsample_url=http://new/b\n")

    def test_output_inside_source_rejected_before_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "roku").mkdir()
            with patch("tools.package.ROOT", root), self.assertRaises(ValueError):
                build(root / "roku/output.zip")
            self.assertFalse((root / "roku/output.zip").exists())

    def test_missing_manifest_does_not_replace_existing_package(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "roku").mkdir()
            output = root / "out.zip"
            output.write_bytes(b"previous package")
            with patch("tools.package.ROOT", root), self.assertRaises(ValueError):
                build(output)
            self.assertEqual(output.read_bytes(), b"previous package")

    def test_hidden_files_and_symlinks_not_shipped(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "roku").mkdir()
            (root / "roku/manifest").write_text("title=Test\nsample_url=\n")
            (root / "roku/.DS_Store").write_bytes(b"junk")
            (root / "roku/.private").mkdir()
            (root / "roku/.private/secret").write_bytes(b"private")
            secret = root / "private.txt"
            secret.write_bytes(b"private")
            (root / "roku/linked.txt").symlink_to(secret)
            with patch("tools.package.ROOT", root):
                output = root / "out.zip"
                build(output)
                with ZipFile(output) as archive:
                    self.assertEqual(archive.namelist(), ["manifest"])

    def test_failed_build_preserves_previous_package(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "roku").mkdir()
            (root / "roku/manifest").write_text("title=Test\nsample_url=\n")
            (root / "roku/code.brs").write_text("source")
            output = root / "out.zip"
            output.write_bytes(b"previous package")
            with patch("tools.package.ROOT", root), patch.object(
                    Path, "read_bytes", side_effect=OSError("unreadable source")):
                with self.assertRaises(OSError):
                    build(output)
            self.assertEqual(output.read_bytes(), b"previous package")
            self.assertEqual(list(root.glob("*.tmp")), [])

    def test_missing_or_duplicate_sample_url_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "roku").mkdir()
            for content in ["title=Test\n", "sample_url=\nsample_url=\n"]:
                (root / "roku/manifest").write_text(content)
                with patch("tools.package.ROOT", root), self.assertRaises(ValueError):
                    build(root / "out.zip")
