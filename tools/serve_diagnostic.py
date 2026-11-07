"""Serve only the diagnostic MP4, with byte ranges for Roku seeking."""
import argparse
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def byte_range(value: str, size: int) -> tuple[int, int]:
    match = re.fullmatch(r"bytes=(\d*)-(\d*)", value)
    if not match or size <= 0:
        raise ValueError("Invalid range")
    first, last = match.groups()
    if not first:
        if not last or int(last) <= 0:
            raise ValueError("Invalid suffix range")
        return max(0, size - int(last)), size - 1
    start = int(first)
    end = min(int(last), size - 1) if last else size - 1
    if start >= size or end < start:
        raise ValueError("Unsatisfiable range")
    return start, end


def handler_for(clip: Path):
    class DiagnosticHandler(BaseHTTPRequestHandler):
        def do_HEAD(self):
            self.serve_clip(body=False)

        def do_GET(self):
            self.serve_clip(body=True)

        def serve_clip(self, body: bool):
            if urlsplit(self.path).path != "/diagnostic.mp4":
                self.send_error(404)
                return
            try:
                stream = clip.open("rb")
            except OSError:
                self.send_error(404, "Diagnostic clip missing")
                return
            with stream:
                stream.seek(0, 2)
                size = stream.tell()
                start, end = 0, size - 1
                # Range applies to GET only; HEAD describes the entire resource.
                requested_range = self.headers.get("Range") if body else None
                if requested_range:
                    try:
                        start, end = byte_range(requested_range, size)
                    except ValueError:
                        self.send_response(416)
                        self.send_header("Content-Range", f"bytes */{size}")
                        self.send_header("Content-Length", "0")
                        self.end_headers()
                        return
                self.send_response(206 if requested_range else 200)
                self.send_header("Content-Type", "video/mp4")
                self.send_header("Accept-Ranges", "bytes")
                self.send_header("Content-Length", str(end - start + 1))
                if requested_range:
                    self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
                self.end_headers()
                if not body:
                    return
                stream.seek(start)
                remaining = end - start + 1
                try:
                    while remaining > 0:
                        chunk = stream.read(min(65536, remaining))
                        if not chunk:
                            break
                        self.wfile.write(chunk)
                        remaining -= len(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    # Roku can cancel the current download when seeking or leaving.
                    return

    return DiagnosticHandler


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bind", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    clip = ROOT / "media/diagnostic.mp4"
    if not clip.is_file():
        parser.error("Run sh tools/make_diagnostic.sh first")
    with ThreadingHTTPServer((args.bind, args.port), handler_for(clip)) as server:
        print(f"Serving diagnostic.mp4 on {args.bind}:{args.port} with byte ranges", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
