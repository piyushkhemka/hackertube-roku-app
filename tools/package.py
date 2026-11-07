"""Build a deterministic developer-installable ZIP; never a signed Roku package."""
import argparse
import hashlib
from pathlib import Path
from urllib.parse import urlsplit
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]


def build(output: Path, sample_url: str = "") -> str:
    if sample_url:
        parsed = urlsplit(sample_url)
        if (parsed.scheme not in {"http", "https"} or not parsed.hostname
                or parsed.username or parsed.password
                or any(c.isspace() for c in sample_url)):
            raise ValueError("sample URL must be HTTP(S), without credentials or whitespace")
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted((ROOT / "roku").rglob("*")):
            if not path.is_file():
                continue
            name = path.relative_to(ROOT / "roku").as_posix()
            data = path.read_bytes()
            if name == "manifest":
                data = data.replace(b"sample_url=", ("sample_url=" + sample_url).encode())
            info = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(f"{digest}  {output.name}\n")
    return digest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample-url", default="")
    parser.add_argument("--output", type=Path, default=ROOT / "dist/hackertube-roku-m0.zip")
    args = parser.parse_args()
    print(build(args.output, args.sample_url))
