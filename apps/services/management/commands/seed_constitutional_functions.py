"""
Seed the 14 ConstitutionalFunction records from the Fourth Schedule
of the Constitution of Kenya (2010), Part 2 — County Government Functions.
"""
from django.core.management.base import BaseCommand
from apps.services.models import ConstitutionalFunction
from core.constitutional_services import COUNTY_FUNCTIONS


class Command(BaseCommand):
    help = 'Seed the 14 county constitutional functions from the Fourth Schedule.'

    def handle(self, **options):
        created = 0
        updated = 0

        for i, fn in enumerate(COUNTY_FUNCTIONS):
            obj, is_new = ConstitutionalFunction.objects.update_or_create(
                code=fn['id'],
                defaults={
                    'name': fn['name'],
                    'description': fn['description'],
                    'mandate_ref': fn['mandate_ref'],
                    'icon': fn['icon'],
                    'order': i + 1,
                    'is_active': True,
                },
            )
            if is_new:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Constitutional functions: {created} created, {updated} updated '
            f'({ConstitutionalFunction.objects.count()} total)'
        ))
