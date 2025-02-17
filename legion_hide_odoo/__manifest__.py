# -*- coding: utf-8 -*-
{
    'name': "Hide Odoo Brand In User Account Menu",
    'version': '18.0.0.0',

    "author": "Taknia Soft",
    'company': 'Taknia Soft',
    'maintainer': 'Emad Kadry',
    
    'depends': ['base'],
    'license': 'LGPL-3',
    "category": 'Tools',

    'summary': """Remove Documentation, Support, My Odoo.com account from the top right Menu""",
    'description': """ Remove Documentation, Support, My Odoo.com account from the top right Menu """,

    'assets': {
        'web.assets_backend': [
            'legion_hide_odoo/static/src/js/extended_user_menu.js',
        ],
    },

    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.gif'],
    
}
