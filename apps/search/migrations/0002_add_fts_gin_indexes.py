from django.db import migrations


def _create_gin_indexes(apps, schema_editor):
    if schema_editor.connection.vendor != 'postgresql':
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS services_service_fts_idx
            ON services_service
            USING GIN (
                to_tsvector('english', coalesce(name, '') || ' ' || coalesce(short_description, '') || ' ' || coalesce(description, ''))
            )
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS search_searchindex_fts_idx
            ON search_searchindex
            USING GIN (
                to_tsvector('english', coalesce(title, '') || ' ' || coalesce(description, ''))
            )
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS news_newsarticle_fts_idx
            ON news_newsarticle
            USING GIN (
                to_tsvector('english', coalesce(title, '') || ' ' || coalesce(summary, ''))
            )
        """)


def _drop_gin_indexes(apps, schema_editor):
    if schema_editor.connection.vendor != 'postgresql':
        return
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("DROP INDEX IF EXISTS services_service_fts_idx")
        cursor.execute("DROP INDEX IF EXISTS search_searchindex_fts_idx")
        cursor.execute("DROP INDEX IF EXISTS news_newsarticle_fts_idx")


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
        ('services', '__first__'),
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(_create_gin_indexes, _drop_gin_indexes, elidable=True),
    ]
