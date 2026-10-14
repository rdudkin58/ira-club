#!/usr/bin/env python3
"""Extract the newest uploaded 16-card story ZIP into the published site root.

Only whitelisted filenames are accepted. Nothing is deleted.
"""
from pathlib import Path
from zipfile import ZipFile, BadZipFile
import re
import struct
import subprocess
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
UPLOADS = ROOT / "uploads" / "stories"
FILE_RE = re.compile(r"irina-story-(0[1-9]|1[0-6])\.png\Z")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 8 * 1024 * 1024
MAX_ARCHIVE_BYTES = 55 * 1024 * 1024

def git_last_commit(path: Path) -> int:
    rel = path.relative_to(ROOT).as_posix()
    completed = subprocess.run(
        ["git", "log", "-1", "--format=%ct", "--", rel],
        cwd=ROOT, text=True, capture_output=True, check=True
    )
    return int(completed.stdout.strip() or "0")

archives = [p for p in UPLOADS.glob("*.zip") if p.stat().st_size <= MAX_ARCHIVE_BYTES]
manifest = ROOT / 'stories-495-manifest.json'
retired = set()
if manifest.exists():
    retired = set(json.loads(manifest.read_text())['superseded_zip_sha256'])
archives = [p for p in archives if hashlib.sha256(p.read_bytes()).hexdigest() not in retired]
if not archives:
    print("No new ZIP archives; directly published images remain unchanged.")
    raise SystemExit(0)
archive = max(archives, key=lambda p: (git_last_commit(p), p.name))
print(f"Selected upload: {archive.relative_to(ROOT)}")
with ZipFile(archive, "r") as bundle:
    entries = {Path(i.filename).name: i for i in bundle.infolist() if not i.is_dir()}
    expected = {f"irina-story-{i:02d}.png" for i in range(1, 17)}
    if set(entries) != expected:
        raise SystemExit(f"ZIP must contain exactly {sorted(expected)}; got {sorted(entries)}")
    for filename in sorted(expected):
        info = entries[filename]
        if info.file_size > MAX_BYTES:
            raise SystemExit(f"File too large: {filename}")
        contents = bundle.read(info)
        if not contents.startswith(PNG_SIGNATURE) or len(contents) < 24:
            raise SystemExit(f"Invalid PNG: {filename}")
        width, height = struct.unpack(">II", contents[16:24])
        if (width, height) != (1080, 1920):
            raise SystemExit(f"Unexpected size of {filename}: {width}x{height}")
        (ROOT / filename).write_bytes(contents)
        print("Wrote", filename)

print("All 16 validated images extracted.")
