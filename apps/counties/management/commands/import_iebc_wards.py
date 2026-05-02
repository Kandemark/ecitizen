"""
Import Kenya ward data from the alvinchesaro JSON source plus supplementary
data for missing counties. Idempotent — skips existing records.

Source: https://github.com/alvinchesaro/Kenya-Counties-SubCounties-and-Wards

Usage:
    python manage.py import_iebc_wards
    python manage.py import_iebc_wards --dry-run
"""
import json
from pathlib import Path
from django.core.management.base import BaseCommand
from apps.counties.models import County, SubCounty, Ward
from apps.counties.data.kenya_locations import COUNTY_META, SUB_COUNTIES as LEGACY_DATA


SOURCE_FILE = Path(__file__).resolve().parent.parent.parent / 'data' / 'kenya_wards_source.json'

# Build a normalized name→code lookup for fuzzy matching JSON county names.
def _normalize(s):
    """Strip everything but a-z for comparison."""
    return ''.join(c for c in s.lower() if 'a' <= c <= 'z')

NAME_TO_CODE = {}
for code, (name, *_) in COUNTY_META.items():
    NAME_TO_CODE[_normalize(name)] = code

# "Keroka" in the JSON is not a real county — it's a town in Nyamira/Kisii.
# We skip it since Nyamira and Kisii are both already in the JSON.


class Command(BaseCommand):
    help = 'Import IEBC wards from JSON source and fill missing counties from legacy data.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Show what would be imported.')

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        if not SOURCE_FILE.exists():
            self.stderr.write(f'Source file not found: {SOURCE_FILE}')
            return

        with open(SOURCE_FILE) as f:
            json_data = json.load(f)

        # Stats
        stats = {'counties': 0, 'sub_counties': 0, 'wards': 0, 'skipped': 0}
        covered = set()  # track county codes processed from JSON

        # ---- Step 1: JSON source ----
        for county_name, sub_counties_dict in json_data.items():
            code = self._resolve_code(county_name)
            if code is None:
                self.stdout.write(self.style.WARNING(
                    f'  SKIP "{county_name}" — not mappable to a county code'
                ))
                stats['skipped'] += 1
                continue

            covered.add(code)
            county, cc = self._get_or_create_county(code, dry_run)
            if cc:
                stats['counties'] += 1

            for sc_idx, (sc_name, ward_names) in enumerate(sub_counties_dict.items(), 1):
                sc_code = f'{code}{sc_idx:02d}'
                sub_county, sc_created = self._get_or_create_sub_county(
                    sc_code, sc_name, county, dry_run
                )
                if sc_created:
                    stats['sub_counties'] += 1

                for w_idx, ward_name in enumerate(ward_names, 1):
                    w_code = f'{sc_code}{w_idx:02d}'
                    _, w_created = self._get_or_create_ward(
                        w_code, ward_name, sub_county, dry_run
                    )
                    if w_created:
                        stats['wards'] += 1

        # ---- Step 2: Fill missing counties from legacy data ----
        for code in sorted(COUNTY_META.keys()):
            if code not in covered:
                county, cc = self._get_or_create_county(code, dry_run)
                if cc:
                    stats['counties'] += 1
                sub_data = LEGACY_DATA.get(code, [])
                for sc_code, sc_name, wards in sub_data:
                    sub_county, sc_created = self._get_or_create_sub_county(
                        sc_code, sc_name, county, dry_run
                    )
                    if sc_created:
                        stats['sub_counties'] += 1
                    for w_code, w_name, villages in wards:
                        _, w_created = self._get_or_create_ward(
                            w_code, w_name, sub_county, dry_run
                        )
                        if w_created:
                            stats['wards'] += 1
                    # Also seed villages for these counties
                    for w_code, w_name, villages in wards:
                        ward = Ward.objects.filter(code=w_code).first()
                        if ward:
                            for v_code, v_name in villages:
                                from apps.counties.models import Village
                                _, vc = Village.objects.get_or_create(
                                    code=v_code,
                                    defaults={'name': v_name, 'ward': ward},
                                )

        self.stdout.write(self.style.SUCCESS(
            f'\nImported: {stats["counties"]} counties, {stats["sub_counties"]} sub-counties, '
            f'{stats["wards"]} wards. Skipped: {stats["skipped"]} unmappable entries.'
            + (' (DRY RUN)' if dry_run else '')
        ))

    def _resolve_code(self, county_name):
        """Map a county name from the JSON to our 3-digit code via normalization."""
        return NAME_TO_CODE.get(_normalize(county_name))

    def _get_or_create_county(self, code, dry_run):
        meta = COUNTY_META.get(code)
        if not meta:
            return None, False
        name, capital, governor, population, area = meta
        if dry_run:
            exists = County.objects.filter(code=code).exists()
            if not exists:
                self.stdout.write(f'  + County: {name} ({code})')
            return None, not exists
        obj, created = County.objects.get_or_create(
            code=code,
            defaults={
                'name': name, 'capital': capital, 'governor': governor,
                'population': population, 'area_sqkm': area,
            },
        )
        if created:
            self.stdout.write(f'  + County: {name} ({code})')
        return obj, created

    def _get_or_create_sub_county(self, code, name, county, dry_run):
        if dry_run:
            exists = SubCounty.objects.filter(code=code).exists()
            if not exists:
                self.stdout.write(f'    + Sub-County: {name} ({code})')
            return None, not exists
        obj, created = SubCounty.objects.get_or_create(
            code=code,
            defaults={'name': name, 'county': county},
        )
        if created:
            self.stdout.write(f'    + Sub-County: {name} ({code})')
        return obj, created

    def _get_or_create_ward(self, code, name, sub_county, dry_run):
        if dry_run:
            exists = Ward.objects.filter(code=code).exists()
            if not exists:
                self.stdout.write(f'      + Ward: {name} ({code})')
            return None, not exists
        obj, created = Ward.objects.get_or_create(
            code=code,
            defaults={'name': name, 'sub_county': sub_county},
        )
        if created:
            self.stdout.write(f'      + Ward: {name} ({code})')
        return obj, created
