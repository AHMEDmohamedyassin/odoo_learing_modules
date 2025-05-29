# -*- coding: utf-8 -*-
{
    'name': "my_module",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base' , 'contacts' , 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/contact_view.xml',
        'views/property_state_history_view.xml',
        'wizard/change_property_state_wizard.xml',
        'reports/property_report.xml',
        'data/sequence.xml',
    ],

    # assets
    'assets': {
        'web.assets_backend': [
            # CSS files first
            'my_module/static/dist/css/main.css',
            'my_module/static/src/components/listView/listView.css',
            # XML template before JS
            'my_module/static/src/components/listView/listView.xml',
            # JS files last
            'my_module/static/src/components/listView/listView.js',
        ],
    },

}

