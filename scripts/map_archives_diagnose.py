import json
import os

from django.conf import settings

from core.models import Monastery

base = settings.BASE_DIR
json_path = os.path.join(base, 'static', 'data', 'archives.json')
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print('Diagnosing entries:')
for entry in data.get('archives', []):
    title = entry.get('title')
    monastery_name = entry.get('monastery')
    m = Monastery.objects.filter(name__iexact=monastery_name).first() or Monastery.objects.filter(name__icontains=monastery_name).first()
    print('-', title, '-> monastery found' if m else '-> monastery NOT found (looked for: "{}")'.format(monastery_name))
