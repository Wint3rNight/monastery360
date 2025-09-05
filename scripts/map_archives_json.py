"""Map entries in static/data/archives.json to archives:item_download endpoints when a confident DB match exists.

Usage: run via `python manage.py shell -c "__import__('runpy').run_path('scripts/map_archives_json.py')"`
"""
import json
import os

from django.conf import settings
from django.urls import reverse

from archives.models import ArchiveItem
from core.models import Monastery

base = settings.BASE_DIR
json_path = os.path.join(base, 'static', 'data', 'archives.json')
backup_path = json_path + '.bak'

print('Loading', json_path)
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Backup
if not os.path.exists(backup_path):
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print('Backup created at', backup_path)

archives = data.get('archives', [])
updated = 0
skipped = 0
changes = []

for entry in archives:
    title = entry.get('title', '').strip()
    monastery_name = entry.get('monastery', '').strip()
    orig = entry.get('downloadUrl')
    if not title or not monastery_name:
        skipped += 1
        continue

    # Try to find monastery slug
    monastery = Monastery.objects.filter(name__iexact=monastery_name).first()
    if not monastery:
        # try partial match
        monastery = Monastery.objects.filter(name__icontains=monastery_name).first()
    if not monastery:
        skipped += 1
        continue

    # Try to find ArchiveItem by title and monastery
    item = ArchiveItem.objects.filter(monastery=monastery, title__iexact=title).first()
    if not item:
        item = ArchiveItem.objects.filter(monastery=monastery, title__icontains=title).first()
    if not item:
        skipped += 1
        continue

    # Build download URL
    new_url = reverse('archives:item_download', kwargs={'monastery_slug': monastery.slug, 'catalog_number': item.catalog_number})
    if orig != new_url:
        entry['downloadUrl'] = new_url
        updated += 1
        changes.append({'title': title, 'monastery': monastery.name, 'old': orig, 'new': new_url})

print(f'Updated {updated} entries, skipped {skipped} entries')
if changes:
    print('Changes:')
    for c in changes:
        print('-', c['title'], '@', c['monastery'], '->', c['new'])

# Write back
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print('Wrote updates to', json_path)
