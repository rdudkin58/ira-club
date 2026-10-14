#!/usr/bin/env python3
"""Emit a bounded base64 chunk for the authenticated GitHub connector.

No tokens or external services are needed. The orchestrator concatenates chunks
in memory and passes them directly to GitHub create_blob(encoding='base64').
"""
import argparse
import base64
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('file', type=Path)
p.add_argument('--offset', type=int, default=0)
p.add_argument('--size', type=int, default=120000)
a = p.parse_args()
if a.offset < 0 or not 1 <= a.size <= 120000:
    p.error('invalid chunk bounds')
with a.file.open('rb') as f:
    f.seek(a.offset)
    data = f.read(a.size)
print(json.dumps({'base64': base64.b64encode(data).decode('ascii'),
                  'bytes': len(data), 'total': a.file.stat().st_size}))
