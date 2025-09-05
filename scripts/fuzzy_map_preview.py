"""Fuzzy preview mapping of static/data/archives.json entries to archives:item_download endpoints.
Writes a proposals file at scripts/proposed_mappings.json and prints a human-readable preview.
"""
import json
import os
from difflib import SequenceMatcher, get_close_matches

from django.conf import settings
from django.urls import reverse

from archives.models import ArchiveItem
from core.models import Monastery

BASE = settings.BASE_DIR
JSON_PATH = os.path.join(BASE, 'static', 'data', 'archives.json')
PROPOSAL_PATH = os.path.join(BASE, 'scripts', 'proposed_mappings.json')

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

archives = data.get('archives', [])

# Pull list of monasteries from DB
monasteries = list(Monastery.objects.all())
monastery_names = [m.name for m in monasteries]

proposals = []

# thresholds
MONASTERY_THRESH = 0.65
TITLE_THRESH = 0.55

print('\nFuzzy mapping preview')
print('Monasteries in DB:', len(monastery_names))
print('Entries to check:', len(archives))

for entry in archives:
    title = (entry.get('title') or '').strip()
    monastery_name = (entry.get('monastery') or '').strip()
    orig_url = entry.get('downloadUrl')

    # find best monastery match by name similarity
    best_mon = None
    best_mon_score = 0.0
    if monastery_name:
        for m in monasteries:
            score = SequenceMatcher(None, monastery_name.lower(), (m.name or '').lower()).ratio()
            if score > best_mon_score:
                best_mon_score = score
                best_mon = m

    # find best archive item within that monastery
    best_item = None
    best_title_score = 0.0
    if best_mon and title:
        items = ArchiveItem.objects.filter(monastery=best_mon)
        for it in items:
            score = SequenceMatcher(None, title.lower(), (it.title or '').lower()).ratio()
            if score > best_title_score:
                best_title_score = score
                best_item = it

    ok = False
    new_url = None
    reason = []
    if best_mon_score >= MONASTERY_THRESH:
        reason.append(f"monastery_match={best_mon.name}({best_mon_score:.2f})")
    else:
        reason.append(f"monastery_nomatch({best_mon_score:.2f})")
    if best_item and best_title_score >= TITLE_THRESH:
        reason.append(f"title_match={best_item.catalog_number}({best_title_score:.2f})")
        new_url = reverse('archives:item_download', kwargs={'monastery_slug': best_mon.slug, 'catalog_number': best_item.catalog_number})
        ok = True
    else:
        if best_item:
            reason.append(f"title_nomatch({best_title_score:.2f})")
        else:
            reason.append('no_items_in_monastery')

    proposal = {
        'title': title,
        'monastery_name': monastery_name,
        'original_downloadUrl': orig_url,
        'proposed_downloadUrl': new_url,
        'ok': ok,
        'reason': reason
    }
    proposals.append(proposal)

# Write proposals file
with open(PROPOSAL_PATH, 'w', encoding='utf-8') as f:
    json.dump(proposals, f, indent=2, ensure_ascii=False)

# Print summary
changed = [p for p in proposals if p['ok']]
print(f'\nProposals found: {len(changed)} entries mapped confidently')
for p in changed:
    print('-', p['title'], '@', p['monastery_name'], '->', p['proposed_downloadUrl'], '|', ','.join(p['reason']))

print(f'\nWrote proposals to {PROPOSAL_PATH}')
print('To apply these changes automatically, run the advertised apply script (not created yet).')
