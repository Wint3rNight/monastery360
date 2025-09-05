import json
from pathlib import Path

from django.core.management.base import BaseCommand

from core.models import Monastery


class Command(BaseCommand):
    help = 'Populate pano_id for Monastery records from static/data/monasteries.json'

    def handle(self, *args, **options):
        data_path = Path('static/data/monasteries.json')
        if not data_path.exists():
            self.stderr.write(f'File not found: {data_path}')
            return

        with data_path.open() as f:
            payload = json.load(f)

        mapping = {}
        for m in payload.get('monasteries', []):
            key = (m.get('name') or '').strip().lower()
            mapping[key] = m.get('panoId')
            slug_key = (m.get('panoId') or '').strip().lower()
            mapping[slug_key] = m.get('panoId')

        updated = 0
        for monastery in Monastery.objects.all():
            name_key = monastery.name.strip().lower()
            pano = mapping.get(name_key) or mapping.get(monastery.slug.lower())
            if pano and monastery.pano_id != pano:
                monastery.pano_id = pano
                monastery.save(update_fields=['pano_id'])
                updated += 1
                self.stdout.write(f'Updated {monastery.name} -> {pano}')

        self.stdout.write(self.style.SUCCESS(f'Done. {updated} monasteries updated.'))
