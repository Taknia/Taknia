# -*- coding: utf-8 -*-
# Copyright (C) Quocent Pvt. Ltd.
# All Rights Reserved
{
    'name': 'Streamlined User Account Menu',
    'version': '18.0.0.0.0',
    'license': 'LGPL-3',
    'category': 'Tools',
    'summary': 'Enhances the Odoo user account menu by removing unnecessary options.',
    'description': """
        This module streamlines the user account menu in Odoo by removing unnecessary options,
        providing a cleaner and more focused user experience. Ideal for businesses looking to 
        declutter their Odoo instance and maintain a professional environment.
    """,
    'author': "Quocent Pvt. Ltd.",
    'website': "https://www.quocent.com",
    'depends': ['web'],
    'data': [
        # Add your XML/CSV files here for menu customizations, views, etc.
    ],
    'assets': {
        'web.assets_backend': [
            'qcent_refined_user_account_menu/static/src/js/user_menu_items.js',  # Path to your custom JS file
        ],
    },
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
