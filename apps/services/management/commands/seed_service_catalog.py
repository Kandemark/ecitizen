"""
Seed the service catalog with required documents, eligibility rules,
and ministry departments — the metadata that makes services "real".
"""
from django.core.management.base import BaseCommand
from apps.services.models import Service, ServiceCategory, EligibilityRule, RequiredDocument
from apps.ministries.models import Ministry, Department


REQUIRED_DOCUMENTS = [
    # Generic docs used across many services
    ('national_id', 'National ID Card', 'Valid Kenyan National Identity Card (original + copy)', True),
    ('passport_photo', 'Passport-size Photo', 'Recent color photograph, white background, 2x2 inches', True),
    ('birth_cert', 'Birth Certificate', 'Certified copy of birth certificate', True),
    ('kra_pin', 'KRA PIN Certificate', 'Kenya Revenue Authority Personal Identification Number', True),
    ('police_clearance', 'Police Clearance Certificate', 'Certificate of Good Conduct from Directorate of Criminal Investigations', False),
    ('passport_doc', 'Valid Passport', 'Current valid Kenyan passport', True),
    ('marriage_cert', 'Marriage Certificate', 'Certified copy of marriage certificate', False),
    ('academic_cert', 'Academic Certificate', 'Relevant academic or professional qualification certificate', True),
    ('kra_compliance', 'Tax Compliance Certificate', 'Valid KRA Tax Compliance Certificate', False),
    ('business_reg', 'Business Registration Certificate', 'Certificate of Business Registration / Incorporation', True),
    ('title_deed', 'Title Deed', 'Original title deed or certificate of lease', True),
    ('consent_letter', 'Consent Letter', 'Signed consent letter from relevant party or authority', False),
    ('medical_report', 'Medical Report', 'Report from a licensed medical practitioner', False),
    ('logbook', 'Vehicle Logbook', 'Original vehicle logbook (registration book)', True),
    ('driving_school_cert', 'Driving School Certificate', 'Certificate of completion from a licensed driving school', True),
    ('company_memo', 'Memorandum & Articles of Association', 'Company constitutional documents', True),
    ('cr12', 'CR12 Form', 'Company directorship details from Registrar of Companies', False),
    ('survey_plan', 'Survey Plan', 'Approved survey plan from Directorate of Surveys', False),
    ('valuation_report', 'Valuation Report', 'Property valuation report from a registered valuer', False),
    ('work_permit_doc', 'Work Permit', 'Valid work permit or dependent pass', False),
    ('visa_doc', 'Visa', 'Valid visa or entry permit', False),
    ('recommendation_letter', 'Letter of Recommendation', 'Recommendation from relevant professional body or institution', False),
    ('proof_payment', 'Proof of Payment', 'Receipt or transaction confirmation of fee payment', True),
    ('application_form', 'Completed Application Form', 'Duly filled and signed application form', True),
    ('sworn_affidavit', 'Sworn Affidavit', 'Notarized affidavit sworn before a Commissioner for Oaths', False),
]

ELIGIBILITY_RULES = [
    ('adult_kenyan', 'Adult Kenyan Citizen', 'Must be a Kenyan citizen aged 18 years or above', {'min_age': 18, 'kenyan_citizen_only': True}),
    ('any_age_kenyan', 'Kenyan Citizen (Any Age)', 'Must be a Kenyan citizen of any age', {'min_age': 0, 'kenyan_citizen_only': True}),
    ('adult_any', 'Adult (Any Nationality)', 'Must be aged 18 years or above', {'min_age': 18, 'kenyan_citizen_only': False}),
    ('minor_kenyan', 'Minor Kenyan Citizen', 'Must be a Kenyan citizen under 18 years of age', {'min_age': 0, 'max_age': 17, 'kenyan_citizen_only': True}),
    ('registered_business', 'Registered Business', 'Must be a business registered in Kenya', {'min_age': 0, 'kenyan_citizen_only': False}),
    ('licensed_professional', 'Licensed Professional', 'Must hold a valid professional practicing license', {'min_age': 21, 'kenyan_citizen_only': False}),
    ('land_owner', 'Land Owner', 'Must be the registered owner or legal representative of the property', {'min_age': 18, 'kenyan_citizen_only': False}),
    ('tax_registered', 'Tax Registered', 'Must have an active KRA PIN and be tax compliant', {'min_age': 18, 'kenyan_citizen_only': False}),
    ('student', 'Student', 'Must be enrolled in or admitted to a recognized institution', {'min_age': 0, 'kenyan_citizen_only': True}),
    ('employer', 'Employer', 'Must be a registered employer or company', {'min_age': 0, 'kenyan_citizen_only': False}),
]

SERVICE_DOCUMENT_MAP = {
    'national-id-application': ['application_form', 'birth_cert', 'passport_photo'],
    'national-id-replacement': ['application_form', 'police_clearance', 'passport_photo', 'sworn_affidavit'],
    'birth-certificate-application': ['application_form', 'national_id'],
    'death-certificate-application': ['application_form', 'national_id', 'medical_report'],
    'civil-marriage-registration': ['application_form', 'national_id', 'passport_photo'],
    'passport-application': ['application_form', 'birth_cert', 'national_id', 'passport_photo', 'recommendation_letter'],
    'passport-renewal': ['application_form', 'passport_doc', 'national_id', 'passport_photo'],
    'visa-application': ['application_form', 'passport_doc', 'passport_photo', 'proof_payment'],
    'work-permit-application': ['application_form', 'passport_doc', 'academic_cert', 'recommendation_letter'],
    'alien-id-card': ['application_form', 'passport_doc', 'visa_doc', 'passport_photo'],
    'driving-license-application': ['application_form', 'national_id', 'driving_school_cert', 'passport_photo', 'medical_report'],
    'driving-license-renewal': ['application_form', 'national_id', 'medical_report', 'passport_photo'],
    'vehicle-registration': ['application_form', 'logbook', 'national_id', 'kra_pin'],
    'motor-vehicle-search': ['application_form', 'logbook', 'national_id'],
    'road-service-license': ['application_form', 'business_reg', 'kra_pin', 'logbook'],
    'land-title-search': ['application_form', 'title_deed', 'national_id'],
    'land-rate-payment': ['application_form', 'title_deed', 'national_id'],
    'land-rent-clearance': ['application_form', 'title_deed', 'national_id', 'proof_payment'],
    'property-transfer-registration': ['application_form', 'title_deed', 'national_id', 'kra_pin', 'valuation_report', 'consent_letter'],
    'survey-plan-approval': ['application_form', 'title_deed', 'survey_plan', 'national_id'],
    'business-name-registration': ['application_form', 'national_id', 'passport_photo', 'kra_pin'],
    'company-incorporation': ['application_form', 'national_id', 'company_memo', 'kra_pin', 'cr12'],
    'single-business-permit': ['application_form', 'business_reg', 'kra_compliance', 'national_id'],
    'export-import-license': ['application_form', 'business_reg', 'kra_compliance', 'kra_pin'],
    'tax-compliance-certificate': ['application_form', 'kra_pin', 'national_id'],
    'nhif-registration': ['application_form', 'national_id', 'passport_photo'],
    'nhif-contribution-payment': ['application_form', 'national_id'],
    'kcpe-kcse-results': ['application_form', 'national_id'],
    'university-admission': ['application_form', 'academic_cert', 'national_id'],
    'medical-practitioner-license': ['application_form', 'academic_cert', 'national_id', 'recommendation_letter', 'passport_photo'],
}

SERVICE_RULE_MAP = {
    'national-id-application': ['any_age_kenyan'],
    'national-id-replacement': ['adult_kenyan'],
    'birth-certificate-application': ['adult_kenyan'],
    'death-certificate-application': ['adult_kenyan'],
    'civil-marriage-registration': ['adult_any'],
    'passport-application': ['any_age_kenyan'],
    'passport-renewal': ['adult_kenyan'],
    'visa-application': ['adult_any'],
    'work-permit-application': ['adult_any'],
    'alien-id-card': ['adult_any'],
    'driving-license-application': ['adult_any'],
    'driving-license-renewal': ['adult_any'],
    'vehicle-registration': ['adult_any'],
    'motor-vehicle-search': ['adult_any'],
    'road-service-license': ['licensed_professional'],
    'land-title-search': ['adult_any'],
    'land-rate-payment': ['land_owner'],
    'land-rent-clearance': ['land_owner'],
    'property-transfer-registration': ['land_owner'],
    'survey-plan-approval': ['land_owner'],
    'business-name-registration': ['adult_kenyan'],
    'company-incorporation': ['adult_kenyan'],
    'single-business-permit': ['registered_business'],
    'export-import-license': ['registered_business'],
    'tax-compliance-certificate': ['tax_registered'],
    'nhif-registration': ['any_age_kenyan'],
    'nhif-contribution-payment': ['adult_kenyan'],
    'kcpe-kcse-results': ['student'],
    'university-admission': ['student'],
    'medical-practitioner-license': ['licensed_professional'],
}

DEPARTMENTS = {
    'Ministry of Interior and National Administration': [
        ('Civil Registration', 'cr', 'Birth, death, marriage certificates and civil documentation'),
        ('National Registration Bureau', 'nrb', 'National ID issuance and population register'),
        ('Immigration Services', 'immigration', 'Passports, visas, work permits, citizenship'),
        ('Refugee Affairs', 'refugee', 'Refugee registration and services'),
    ],
    'Ministry of Finance and National Planning': [
        ('Revenue & Taxation', 'revenue', 'Tax policy, revenue collection oversight'),
        ('Economic Planning', 'planning', 'National development planning and budgeting'),
        ('Public Procurement', 'procurement', 'Government procurement regulation and oversight'),
    ],
    'Ministry of Health': [
        ('NHIF', 'nhif', 'National Hospital Insurance Fund'),
        ('Medical Services', 'medical', 'Public health facilities and medical services'),
        ('Public Health', 'public_health', 'Disease prevention, sanitation, health promotion'),
        ('Health Professions', 'health_professions', 'Medical practitioner licensing and regulation'),
    ],
    'Ministry of Education': [
        ('Basic Education', 'basic_edu', 'Primary and secondary education'),
        ('Higher Education', 'higher_edu', 'University and tertiary education, HELB'),
        ('TVET', 'tvet', 'Technical and vocational education and training'),
        ('Examinations', 'examinations', 'KCPE, KCSE, and national examinations'),
    ],
    'Ministry of Lands, Public Works, Housing and Urban Development': [
        ('Land Registration', 'land_reg', 'Title deed registration, land records'),
        ('Survey and Mapping', 'survey', 'Land surveys, mapping, spatial data'),
        ('Housing', 'housing', 'Public housing, building standards'),
        ('Public Works', 'works', 'Government buildings and infrastructure'),
    ],
    'Ministry of Transport and Infrastructure': [
        ('Road Transport & Safety', 'rts', 'Driving licenses, vehicle registration, road safety (NTSA)'),
        ('Railways', 'railways', 'Railway transport regulation'),
        ('Maritime', 'maritime', 'Ports, shipping, maritime affairs'),
        ('Aviation', 'aviation', 'Civil aviation regulation'),
    ],
}


class Command(BaseCommand):
    help = 'Seed service catalog with required documents, eligibility rules, and departments.'

    def handle(self, **options):
        self._seed_departments()
        self._seed_eligibility_rules()
        self._seed_required_documents()
        self._wire_documents_and_rules()
        self.stdout.write(self.style.SUCCESS(
            'Service catalog seeded: docs, rules, and departments wired.'
        ))

    def _seed_departments(self):
        created = 0
        for ministry_name, depts in DEPARTMENTS.items():
            try:
                ministry = Ministry.objects.get(name=ministry_name)
            except Ministry.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  Ministry not found: {ministry_name}'))
                continue
            for dept_name, code, desc in depts:
                _, is_new = Department.objects.get_or_create(
                    ministry=ministry, code=code,
                    defaults={'name': dept_name, 'description': desc},
                )
                if is_new:
                    created += 1
        self.stdout.write(f'  Departments: {created} created ({Department.objects.count()} total)')

    def _seed_eligibility_rules(self):
        created = 0
        for key, name, desc, extra in ELIGIBILITY_RULES:
            kwargs = {'name': name, 'description': desc}
            kwargs.update(extra)
            rule, is_new = EligibilityRule.objects.get_or_create(
                name=name,
                defaults=kwargs,
            )
            if is_new:
                created += 1
        self.stdout.write(f'  Eligibility Rules: {created} created ({EligibilityRule.objects.count()} total)')

    def _seed_required_documents(self):
        created = 0
        for key, name, desc, mandatory in REQUIRED_DOCUMENTS:
            doc, is_new = RequiredDocument.objects.get_or_create(
                name=name,
                defaults={'document_type': key, 'description': desc, 'is_mandatory': mandatory},
            )
            if is_new:
                created += 1
        self.stdout.write(f'  Required Documents: {created} created ({RequiredDocument.objects.count()} total)')

    def _wire_documents_and_rules(self):
        rules_by_name = {r.name: r for r in EligibilityRule.objects.all()}
        # Build lookup by document_type (shorthand key) since map uses those
        docs_by_key = {}
        for d in RequiredDocument.objects.all():
            for key, name, desc, mandatory in REQUIRED_DOCUMENTS:
                if d.name == name:
                    docs_by_key[key] = d
                    break

        wired = 0
        for slug, doc_keys in SERVICE_DOCUMENT_MAP.items():
            try:
                service = Service.objects.get(slug=slug)
            except Service.DoesNotExist:
                continue
            for dkey in doc_keys:
                doc = docs_by_key.get(dkey)
                if doc and not service.required_documents.filter(id=doc.id).exists():
                    service.required_documents.add(doc)
                    wired += 1

        for slug, rule_names in SERVICE_RULE_MAP.items():
            try:
                service = Service.objects.get(slug=slug)
            except Service.DoesNotExist:
                continue
            for rname in rule_names:
                rule = rules_by_name.get(rname)
                if rule and not service.eligibility_rules.filter(id=rule.id).exists():
                    service.eligibility_rules.add(rule)
                    wired += 1

        self.stdout.write(f'  Wired {wired} document/rule assignments across services')
