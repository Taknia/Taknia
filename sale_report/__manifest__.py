# -*- coding: utf-8 -*-
{
    'name': "sale_report",
    'summary': "Module for generating sales reports",
    'description': "Long description of module's purpose",
    'author': "Taknia Soft",
    'website': "http://www.TakniaSoft.com",
    'category': 'Sales',
    'version': '18.0.1.0.0',
    'depends': ['base', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'LGPL-3',
}
