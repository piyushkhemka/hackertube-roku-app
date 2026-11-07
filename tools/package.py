"""Build a deterministic developer-installable ZIP; never a signed Roku package."""
import argparse
import hashlib
import os
import tempfile
from pathlib import Path
from urllib.parse import urlsplit
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]


def build(output: Path, sample_url: str = "") -> str:
    if sample_url:
        parsed = urlsplit(sample_url)
        # Accessing .port validates both its syntax and its numeric range.
        port = parsed.port
        if (parsed.scheme not in {"http", "https"} or not parsed.hostname
                or parsed.username is not None or parsed.password is not None
                or port == 0
                or any(c.isspace() or ord(c) < 32 or ord(c) == 127 for c in sample_url)):
            raise ValueError("sample URL must be HTTP(S), without credentials or control characters")
    source = (ROOT / "roku").resolve()
    output = output.resolve()
    if output.is_relative_to(source):
        raise ValueError("output must be outside the Roku source directory")
    manifest = source / "manifest"
    if not manifest.is_file() or manifest.is_symlink():
        raise ValueError("Roku source must contain a regular manifest file")
    lines = manifest.read_text(encoding="utf-8").splitlines()
    if sum(line.startswith("sample_url=") for line in lines) != 1:
        raise ValueError("manifest must contain exactly one sample_url entry")
    manifest_data = ("\n".join(
        "sample_url=" + sample_url if line.startswith("sample_url=") else line
        for line in lines
    ) + "\n").encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    # Build beside the destination, then replace only after the ZIP closes cleanly.
    fd, temporary_name = tempfile.mkstemp(dir=output.parent, suffix=".zip.tmp")
    os.close(fd)
    temporary = Path(temporary_name)
    try:
        with ZipFile(temporary, "w", compression=ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(source.rglob("*")):
                relative = path.relative_to(source)
                if (not path.is_file() or path.is_symlink()
                        or any(part.startswith(".") for part in relative.parts)
                        or any(parent.is_symlink() for parent in path.parents if parent != source)):
                    continue
                name = relative.as_posix()
                data = manifest_data if name == "manifest" else path.read_bytes()
                info = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
                info.compress_type = ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, data)
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(f"{digest}  {output.name}\n")
    return digest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample-url", default="")
    parser.add_argument("--output", type=Path, default=ROOT / "dist/hackertube-roku-m0.zip")
    args = parser.parse_args()
    print(build(args.output, args.sample_url))
