{
    'name': 'Real Estate Ads',
    'version': '1.1.1',
    'summary': 'Real Estate module show available properties',
    'description': 'Real Estate module show available properties',
    'category': 'Sales',
    'author': 'Rakib',
    'license': 'AGPL-3',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',

        'data/property_type_data.xml',
        'data/patient_tag_demo_data_load.xml',

        'views/property_view.xml',
        'views/property_type_view.xml',
        'views/property_tag.xml',
        'views/property_offer.xml',
        'views/menu_items.xml',
    ],

    'installable': True,
    'auto_install': False,
}