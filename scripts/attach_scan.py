from django.core.files import File

from archives.models import ArchiveItem

slug = 'dubdi-monastery'
catalog = 'DUBDI-MONASTERY-ARTIFACT-002'

try:
    item = ArchiveItem.objects.get(monastery__slug=slug, catalog_number=catalog)
    with open('media/test/sample.pdf','rb') as f:
        item.scan.save('sample.pdf', File(f), save=True)
    print('Attached sample.pdf to', item)
    print('scan url:', item.scan.url)
except ArchiveItem.DoesNotExist:
    print('ArchiveItem not found:', slug, catalog)
