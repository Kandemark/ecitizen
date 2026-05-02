"""
Management command to populate all 47 Kenyan counties, sub-counties, wards,
and villages into the database. Idempotent — skips existing records.

Usage:
    python manage.py seed_kenya_locations
    python manage.py seed_kenya_locations --county=047  # Nairobi only
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from apps.counties.models import County, SubCounty, Ward, Village
from apps.counties.data.kenya_locations import COUNTY_META, SUB_COUNTIES


class Command(BaseCommand):
    help = 'Seed Kenya administrative boundary data — counties → villages.'

    def add_arguments(self, parser):
        parser.add_argument('--county', type=str, help='Seed a specific county code (e.g. 047).')

    def handle(self, *args, **options):
        county_filter = options.get('county')

        counties_to_seed = [county_filter] if county_filter else sorted(COUNTY_META.keys())

        total_counties = 0
        total_sub_counties = 0
        total_wards = 0
        total_villages = 0

        for code in counties_to_seed:
            if code not in COUNTY_META:
                self.stderr.write(f'Unknown county code: {code}')
                continue

            name, capital, governor, population, area = COUNTY_META[code]
            county, created = County.objects.get_or_create(
                code=code,
                defaults={
                    'name': name,
                    'capital': capital,
                    'governor': governor,
                    'population': population,
                    'area_sqkm': area,
                },
            )
            if created:
                self.stdout.write(f'  + County: {name}')
                total_counties += 1

            sub_data = SUB_COUNTIES.get(code, [])
            for sc_code, sc_name, wards in sub_data:
                sub_county, sc_created = SubCounty.objects.get_or_create(
                    code=sc_code,
                    defaults={'name': sc_name, 'county': county},
                )
                if sc_created:
                    total_sub_counties += 1

                for w_code, w_name, villages in wards:
                    ward, w_created = Ward.objects.get_or_create(
                        code=w_code,
                        defaults={'name': w_name, 'sub_county': sub_county},
                    )
                    if w_created:
                        total_wards += 1

                    for v_code, v_name in villages:
                        _, v_created = Village.objects.get_or_create(
                            code=v_code,
                            defaults={'name': v_name, 'ward': ward},
                        )
                        if v_created:
                            total_villages += 1

        self.stdout.write(self.style.SUCCESS(
            f'\nSeeded: {total_counties} counties, {total_sub_counties} sub-counties, '
            f'{total_wards} wards, {total_villages} villages.'
        ))
