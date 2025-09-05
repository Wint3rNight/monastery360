#!/usr/bin/env python3
import os

# Files to delete
files_to_delete = [
    '/home/winter/Documents/Workspace2/monastery360/templates/react_homepage.html',
    '/home/winter/Documents/Workspace2/monastery360/templates/core/home.html'
]

for file_path in files_to_delete:
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"✅ Deleted: {file_path}")
        else:
            print(f"⚠️  File not found: {file_path}")
    except Exception as e:
        print(f"❌ Error deleting {file_path}: {e}")

print("\n🧹 Cleanup completed!")
