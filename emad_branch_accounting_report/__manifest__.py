{
    'name': 'Taknia Soft - Accounting Reports by EMAD Kadry',
    'version': '1.0',
    'summary': 'Advanced Accounting Reports with Branch, Partner & Currency Filters',
    'description': """
        Custom accounting reports including:
        - General Accounting Report with Branches, Journals, Partners & Currency filters
        - Partner Ledger Report with same filters
        - PDF & Excel output
        - Supports multi-branch structure (Company > Branches)
    """,
    'author': 'EMAD Kadry',
    'company': 'Taknia Soft',
    'website': 'http://www.takniasoft.com',
    'category': 'Accounting',
    'depends': ['account', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'views/branch_accounting_report_view.xml',
        'views/partner_ledger_report_view.xml',
        'wizard/branch_accounting_report_wizard_view.xml',
        'wizard/partner_ledger_report_wizard_view.xml',
        'reports/branch_accounting_report_templates.xml',
        'reports/partner_ledger_report_templates.xml',
        'views/branch_accounting_report_wizard_view.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'branch_accounting_report/static/src/css/custom_report_styles.css',
        ],
    }
}
