#!/usr/bin/env python3
"""
Check archive items and their scan files
"""

import os
import sys

import django

# Add the project directory to Python path
sys.path.append('/home/winter/Documents/Workspace2/monastery360')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monastery360.settings')
django.setup()

from archives.models import ArchiveItem


def check_archive_items():
    print("=== Archive Items Analysis ===\n")

    total_items = ArchiveItem.objects.count()
    items_with_scans = ArchiveItem.objects.exclude(scan='').exclude(scan__isnull=True)

    print(f"Total ArchiveItems: {total_items}")
    print(f"Items with scan files: {items_with_scans.count()}")
    print(f"Items without scans: {total_items - items_with_scans.count()}")

    print("\n=== Sample Items ===")
    for item in ArchiveItem.objects.all()[:10]:
        has_scan = bool(item.scan and item.scan.name)
        print(f"- {item.title} ({item.monastery.name})")
        print(f"  Catalog: {item.catalog_number}")
        print(f"  Scan file: {'✓' if has_scan else '✗'}")
        if has_scan:
            print(f"  File: {item.scan.name}")
        print()

    # Check if any items have download URLs in the JSON data
    print("=== Checking JSON Data Mapping ===")
    import json

    try:
        json_path = '/home/winter/Documents/Workspace2/monastery360/static/data/archives.json'
        with open(json_path, 'r') as f:
            data = json.load(f)

        total_json_items = sum(len(monastery_data) for monastery_data in data.values())
        items_with_download = 0

        for monastery, items in data.items():
            for item in items:
                if 'downloadUrl' in item and item['downloadUrl']:
                    items_with_download += 1

        print(f"Total items in JSON: {total_json_items}")
        print(f"Items with download URLs: {items_with_download}")

    except Exception as e:
        print(f"Error reading JSON: {e}")

if __name__ == '__main__':
    check_archive_items()
