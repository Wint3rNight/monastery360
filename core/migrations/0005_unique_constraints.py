# Generated manually for case-insensitive unique constraints

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20250910_0237'),
    ]

    operations = [
        # Add unique constraint for case-insensitive username
        migrations.RunSQL(
            "CREATE UNIQUE INDEX IF NOT EXISTS unique_username_lower_idx ON auth_user (LOWER(username));",
            reverse_sql="DROP INDEX IF EXISTS unique_username_lower_idx;"
        ),
        # Add unique constraint for case-insensitive email
        migrations.RunSQL(
            "CREATE UNIQUE INDEX IF NOT EXISTS unique_email_lower_idx ON auth_user (LOWER(email));",
            reverse_sql="DROP INDEX IF EXISTS unique_email_lower_idx;"
        ),
    ]
