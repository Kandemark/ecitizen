"""
Transport services — driving licenses, vehicle registration, PSV licenses, inspections.

Constitutional mandate: Chapter 4 (Bill of Rights, Art. 43) — right to accessible
transport. Also national transport policy and road safety regulation.
"""
from core.utils import generate_application_reference
from .models import DrivingLicense, VehicleRegistration, PSVLicense, VehicleInspection


def submit_driving_license(*, user, license_class, blood_group='', **kwargs):
    ref = generate_application_reference('DLN')
    lic = DrivingLicense.objects.create(
        user=user, reference=ref,
        license_class=license_class, blood_group=blood_group,
        status='draft',
    )
    lic.status = 'submitted'
    lic.save(update_fields=['status'])
    return lic


def submit_vehicle_registration(*, user, plate_number, vehicle_make, vehicle_model='',
                                  year_of_manufacture=None, color='', vin='',
                                  engine_number='', **kwargs):
    ref = generate_application_reference('VHL')
    reg = VehicleRegistration.objects.create(
        user=user, reference=ref,
        plate_number=plate_number, vehicle_make=vehicle_make,
        vehicle_model=vehicle_model, year_of_manufacture=year_of_manufacture,
        color=color, vin=vin, engine_number=engine_number,
        status='draft',
    )
    reg.status = 'submitted'
    reg.save(update_fields=['status'])
    return reg


def submit_psv_license(*, user, route, operator_name='', sacco_name='',
                         capacity=0, **kwargs):
    ref = generate_application_reference('PSV')
    lic = PSVLicense.objects.create(
        user=user, reference=ref,
        route=route, operator_name=operator_name,
        sacco_name=sacco_name, capacity=capacity,
        status='draft',
    )
    lic.status = 'submitted'
    lic.save(update_fields=['status'])
    return lic


def submit_vehicle_inspection(*, user, inspection_date=None,
                                inspection_center='', **kwargs):
    ref = generate_application_reference('INSP')
    insp = VehicleInspection.objects.create(
        user=user, reference=ref,
        inspection_date=inspection_date, inspection_center=inspection_center,
        status='draft',
    )
    insp.status = 'submitted'
    insp.save(update_fields=['status'])
    return insp


def get_user_records(user):
    return {
        'licenses': DrivingLicense.objects.filter(user=user).order_by('-created_at'),
        'vehicles': VehicleRegistration.objects.filter(user=user).order_by('-created_at'),
        'psv_licenses': PSVLicense.objects.filter(user=user).order_by('-created_at'),
        'inspections': VehicleInspection.objects.filter(user=user).order_by('-created_at'),
    }
