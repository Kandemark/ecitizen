"""
County government functions as mandated by the Fourth Schedule
of the Constitution of Kenya (2010), Part 2.

Used for:
- Displaying constitutional mandates on county pages
- Matching county government services to the service catalog
- Authority dashboards showing implementation status
"""

COUNTY_FUNCTIONS = [
    {
        'id': 'agriculture',
        'name': 'Agriculture & Livestock',
        'icon': 'tractor',
        'description': 'Crop and animal husbandry, livestock sale yards, county abattoirs, '
                       'plant and animal disease control, fisheries.',
        'mandate_ref': 'Fourth Schedule Part 2, Section 1',
        'functions': [
            'Crop husbandry and agricultural extension services',
            'Animal husbandry and breeding programs',
            'Livestock sale yards and auction markets',
            'County abattoirs and meat inspection services',
            'Plant disease and pest control programs',
            'Animal disease control and vaccination campaigns',
            'Fisheries and aquaculture in county water bodies',
        ],
    },
    {
        'id': 'health',
        'name': 'County Health Services',
        'icon': 'heartbeat',
        'description': 'County health facilities, pharmacies, ambulance services, primary care, '
                       'food vendor licensing, veterinary services, cemeteries, and solid waste disposal.',
        'mandate_ref': 'Fourth Schedule Part 2, Section 2',
        'functions': [
            'County referral hospitals, health centres, and dispensaries',
            'County pharmacy services and medical supplies',
            'Emergency ambulance and patient transport services',
            'Primary health care promotion and outreach',
            'Licensing of food vending and eating establishments',
            'County veterinary services and animal health',
            'Cemeteries, funeral parlours, and crematoria management',
            'Refuse collection, dumpsite management, and solid waste disposal',
            'Street cleaning and public sanitation',
        ],
    },
    {
        'id': 'environment',
        'name': 'Environment & Pollution Control',
        'icon': 'leaf',
        'description': 'Air pollution, noise pollution, public nuisances, and outdoor advertising control.',
        'mandate_ref': 'Fourth Schedule Part 2, Section 3',
        'functions': [
            'Air quality monitoring and pollution control',
            'Noise pollution regulation and enforcement',
            'Public nuisance abatement',
            'Outdoor advertising licensing and control',
            'Environmental impact assessments for county projects',
        ],
    },
    {
        'id': 'culture',
        'name': 'Culture, Entertainment & Amenities',
        'icon': 'users',
        'description': 'Cultural activities, public entertainment, public amenities including '
                       'betting, casinos, racing, liquor licensing, cinemas, libraries, museums, '
                       'sports, and county recreation facilities.',
        'mandate_ref': 'Fourth Schedule Part 2, Section 4',
        'functions': [
            'Cultural activities and heritage promotion',
            'Betting, casinos, and gaming licensing',
            'Horse racing and sports betting regulation',
            'Liquor licensing and control',
            'Cinemas, video shows, and public entertainment licensing',
            'County public libraries and reading programs',
            'Museums and cultural centres',
            'Sports facilities and county recreation programs',
            'County parks, beaches, and public recreation areas',
        ],
    },
    {
        'id': 'transport',
        'name': 'County Transport & Infrastructure',
        'icon': 'road',
        'description': 'County roads, street lighting, traffic and parking management, '
                       'public road transport, ferries and harbours (excluding national/international).',
        'mandate_ref': 'Fourth Schedule Part 2, Section 5',
        'functions': [
            'Construction and maintenance of county roads',
            'Street lighting installation and maintenance',
            'Traffic management and parking regulation',
            'Public road transport licensing (matatus, boda bodas, taxis)',
            'County ferries and lake transport services',
            'County harbours and jetties (excluding national ports)',
            'Non-motorized transport (cycling lanes, pedestrian walkways)',
        ],
    },
    {
        'id': 'animal_welfare',
        'name': 'Animal Control & Welfare',
        'icon': 'paw',
        'description': 'Licensing of dogs, facilities for the accommodation, care, and burial of animals.',
        'mandate_ref': 'Fourth Schedule Part 2, Section 6',
        'functions': [
            'Dog licensing and registration',
            'Stray animal control and impoundment',
            'Animal shelters and care facilities',
            'Animal burial and disposal services',
            'Animal welfare inspections and enforcement',
        ],
    },
    {
        'id': 'trade',
        'name': 'Trade Development & Regulation',
        'icon': 'store',
        'description': 'Markets, trade licences (excluding regulation of professions), '
                       'fair trading practices, local tourism, and cooperative societies.',
        'mandate_ref': 'Fourth Schedule Part 2, Section 7',
        'functions': [
            'Construction and management of county markets',
            'Single business permit and trade licensing',
            'Fair trading practices and consumer protection',
            'Local tourism promotion and development',
            'Cooperative society registration and oversight',
            'Small and medium enterprise (SME) development',
            'Weights and measures inspection',
        ],
    },
    {
        'id': 'planning',
        'name': 'County Planning & Development',
        'icon': 'blueprint',
        'description': 'County statistics, land survey and mapping, boundaries and fencing, '
                       'housing including land administration.',
        'mandate_ref': 'Fourth Schedule Part 2, Section 8',
        'functions': [
            'County physical development planning',
            'County statistical surveys and data collection',
            'Land survey, mapping, and GIS services',
            'Boundary determination and fencing',
            'County housing development and estate management',
            'Site and service scheme administration',
            'Urban and rural planning within the county',
        ],
    },
    {
        'id': 'education',
        'name': 'Pre-Primary & Vocational Education',
        'icon': 'school',
        'description': 'Pre-primary education, village polytechnics, homecraft centres, and childcare facilities.',
        'mandate_ref': 'Fourth Schedule Part 2, Section 9',
        'functions': [
            'Pre-primary (ECD) education management',
            'Village polytechnics and youth training centres',
            'Homecraft centres and skills development',
            'Childcare facilities and day-care centres',
            'Adult and continuing education programs',
        ],
    },
    {
        'id': 'natural_resources',
        'name': 'Natural Resources & Conservation',
        'icon': 'tree',
        'description': 'Implementation of national policies on soil and water conservation and forestry '
                       'at the county level.',
        'mandate_ref': 'Fourth Schedule Part 2, Section 10',
        'functions': [
            'Soil erosion control and conservation',
            'Water catchment protection and management',
            'County forestry programs and tree planting',
            'Implementation of national environmental policies',
            'Natural resource mapping and inventory',
        ],
    },
    {
        'id': 'public_works',
        'name': 'County Public Works & Utilities',
        'icon': 'wrench',
        'description': 'Storm water management systems, water supply services, and sanitation services.',
        'mandate_ref': 'Fourth Schedule Part 2, Section 11',
        'functions': [
            'Storm water drainage systems',
            'Rural and urban water supply services',
            'Sewerage and sanitation services',
            'County public buildings construction and maintenance',
            'Borehole drilling and water resource development',
        ],
    },
    {
        'id': 'disaster',
        'name': 'Fire Fighting & Disaster Management',
        'icon': 'shield',
        'description': 'County fire fighting services, disaster preparedness, and emergency response coordination.',
        'mandate_ref': 'Fourth Schedule Part 2, Section 12',
        'functions': [
            'County fire brigade and fire fighting services',
            'Disaster preparedness and early warning systems',
            'Emergency response coordination at county level',
            'Evacuation planning and management',
            'Post-disaster recovery and rehabilitation',
        ],
    },
    {
        'id': 'drugs_control',
        'name': 'Drug & Pornography Control',
        'icon': 'ban',
        'description': 'Control of drugs, substance abuse, and pornography at the county level.',
        'mandate_ref': 'Fourth Schedule Part 2, Section 13',
        'functions': [
            'Drug and substance abuse prevention programs',
            'County rehabilitation centres',
            'Enforcement of pornography restrictions',
            'Public awareness campaigns on drug abuse',
        ],
    },
    {
        'id': 'participation',
        'name': 'Community Participation & Governance',
        'icon': 'comments',
        'description': 'Ensuring and coordinating the participation of communities and locations '
                       'in governance at the local level.',
        'mandate_ref': 'Fourth Schedule Part 2, Section 14',
        'functions': [
            'Public participation forums and barazas',
            'Ward-level development committees',
            'Citizen engagement in county planning and budgeting',
            'Community grievance and feedback mechanisms',
            'Social accountability and transparency programs',
        ],
    },
]

# County function names to service keywords for matching existing services
COUNTY_FUNCTION_SERVICE_MAP = {
    'agriculture': ['agriculture', 'farming', 'crop', 'livestock', 'fisheries', 'abattoir'],
    'health': ['health', 'hospital', 'clinic', 'pharmacy', 'ambulance', 'medical', 'nhif', 'sanitation'],
    'environment': ['environment', 'pollution', 'air quality', 'noise', 'waste'],
    'culture': ['culture', 'entertainment', 'liquor', 'betting', 'sports', 'library', 'museum', 'park'],
    'transport': ['transport', 'road', 'parking', 'driving', 'vehicle', 'ferry', 'boda', 'matatu'],
    'animal_welfare': ['animal', 'dog', 'veterinary', 'pet'],
    'trade': ['trade', 'business', 'market', 'license', 'permit', 'cooperative', 'tourism'],
    'planning': ['planning', 'land', 'survey', 'housing', 'building', 'construction', 'development'],
    'education': ['education', 'school', 'polytechnic', 'childcare', 'ecd', 'training'],
    'natural_resources': ['forestry', 'conservation', 'water', 'soil', 'environmental'],
    'public_works': ['water', 'sewer', 'sanitation', 'drainage', 'borehole', 'public works'],
    'disaster': ['fire', 'disaster', 'emergency', 'rescue'],
    'drugs_control': ['drug', 'substance', 'rehabilitation', 'pornography'],
    'participation': ['participation', 'governance', 'baraza', 'citizen', 'community'],
}
