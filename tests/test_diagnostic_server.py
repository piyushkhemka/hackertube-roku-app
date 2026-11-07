import tempfile
import threading
import unittest
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path

from tools.serve_diagnostic import handler_for


class DiagnosticServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        cls.content = bytes(range(256)) * 16
        cls.clip = Path(cls.directory.name) / "diagnostic.mp4"
        cls.clip.write_bytes(cls.content)
        handler = handler_for(cls.clip)
        handler.log_message = lambda *args: None
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()
        cls.directory.cleanup()

    def request(self, method="GET", path="/diagnostic.mp4", headers=None):
        connection = HTTPConnection(*self.server.server_address, timeout=5)
        try:
            connection.request(method, path, headers=headers or {})
            response = connection.getresponse()
            return response.status, dict(response.getheaders()), response.read()
        finally:
            connection.close()

    def test_full_clip(self):
        status, headers, body = self.request()
        self.assertEqual(status, 200)
        self.assertEqual(body, self.content)
        self.assertEqual(headers["Accept-Ranges"], "bytes")
        self.assertEqual(headers["Content-Type"], "video/mp4")

    def test_ranges_return_correct_bytes(self):
        for value, start, end in [("bytes=512-1023", 512, 1023),
                                  ("bytes=4000-", 4000, 4095),
                                  ("bytes=-20", 4076, 4095),
                                  ("bytes=4090-9000", 4090, 4095)]:
            with self.subTest(value=value):
                status, headers, body = self.request(headers={"Range": value})
                self.assertEqual(status, 206)
                self.assertEqual(headers["Content-Range"], f"bytes {start}-{end}/4096")
                self.assertEqual(int(headers["Content-Length"]), len(body))
                self.assertEqual(body, self.content[start:end + 1])

    def test_invalid_ranges(self):
        for value in ["bytes=4096-", "bytes=20-10", "bytes=-0", "bytes=-", "bytes=0-1,3-4", "invalid"]:
            with self.subTest(value=value):
                status, headers, body = self.request(headers={"Range": value})
                self.assertEqual(status, 416)
                self.assertEqual(headers["Content-Range"], "bytes */4096")
                self.assertEqual(body, b"")

    def test_head(self):
        status, headers, body = self.request("HEAD", headers={"Range": "bytes=0-10"})
        self.assertEqual(status, 200)
        self.assertEqual(headers["Content-Length"], "4096")
        self.assertEqual(body, b"")

    def test_only_clip_exposed(self):
        for path in ["/", "/../README.md", "/%2e%2e/README.md", "/other.mp4"]:
            with self.subTest(path=path):
                self.assertEqual(self.request(path=path)[0], 404)
