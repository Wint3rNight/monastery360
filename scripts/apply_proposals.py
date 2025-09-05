"""Apply proposals from scripts/proposed_mappings.json to static/data/archives.json for entries marked ok==true.
Creates a timestamped backup before writing.
"""
import json
import os
from datetime import datetime

from django.conf import settings

BASE = settings.BASE_DIR
JSON_PATH = os.path.join(BASE, 'static', 'data', 'archives.json')
PROPOSAL_PATH = os.path.join(BASE, 'scripts', 'proposed_mappings.json')

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

with open(PROPOSAL_PATH, 'r', encoding='utf-8') as f:
    proposals = json.load(f)

archives = data.get('archives', [])
if len(archives) != len(proposals):
    print('Warning: archives length and proposals length differ; aborting to avoid mismatch')
    raise SystemExit(1)

# backup
ts = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
backup_path = JSON_PATH + f'.{ts}.bak'
with open(backup_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print('Backup created at', backup_path)

updated = []
for i, entry in enumerate(archives):
    prop = proposals[i]
    if prop.get('ok') and prop.get('proposed_downloadUrl'):
        old = entry.get('downloadUrl')
        new = prop['proposed_downloadUrl']
        if old != new:
            entry['downloadUrl'] = new
            updated.append({'title': entry.get('title'), 'old': old, 'new': new})

if updated:
    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print('Applied updates for', len(updated), 'entries:')
    for u in updated:
        print('-', u['title'], u['old'], '->', u['new'])
else:
    print('No updates to apply')
