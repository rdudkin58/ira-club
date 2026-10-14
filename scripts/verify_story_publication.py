#!/usr/bin/env python3
"""Verify live gallery and all 16 published PNGs against local checksums."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import struct
from urllib.parse import urljoin
from urllib.request import urlopen

p = argparse.ArgumentParser()
p.add_argument('--base-url', default='https://irina-psiholog.ru/')
a = p.parse_args()
root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'stories-495-manifest.json').read_text())

class Gallery(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images, self.downloads = [], []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'img':
            self.images.append(attrs['src'])
        if tag == 'a' and 'download' in attrs:
            self.downloads.append(attrs['href'])

gallery_url = urljoin(a.base_url, 'stories-495.html')
with urlopen(gallery_url, timeout=30) as response:
    assert response.status == 200
    html = response.read().decode('utf-8')
gallery = Gallery()
gallery.feed(html)
assert len(gallery.images) == len(gallery.downloads) == 16, 'Incomplete live gallery'
assert gallery.images == gallery.downloads, 'Downloads differ from previews'

def verify(pair):
    ref, expected = pair
    assert ref == expected['path'] + '?v=' + expected['sha256'][:12], 'Old gallery reference: ' + ref
    with urlopen(urljoin(gallery_url, ref), timeout=30) as response:
        assert response.status == 200
        data = response.read()
    assert data[:8] == b'\x89PNG\r\n\x1a\n', 'Not a PNG: ' + ref
    assert struct.unpack('>II', data[16:24]) == (1080, 1920), 'Wrong dimensions: ' + ref
    assert hashlib.sha256(data).hexdigest() == expected['sha256'], 'Checksum mismatch: ' + ref
    return expected['path'] + ': HTTP 200, 1080x1920, SHA-256 matches'

with ThreadPoolExecutor(max_workers=4) as pool:
    for result in pool.map(verify, zip(gallery.images, manifest['images'])):
        print(result)
print('PASS: live gallery and all 16 PNG downloads verified')
