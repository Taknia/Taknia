{
    'name': 'EMAD Kadry - Branch & Partner Accounting Reports',
    'version': '1.0',
    'summary': 'Custom Accounting Reports for Branches and Partners - Taknia Soft',
    'description': """
        Comprehensive Accounting Reports for Branches and Partners.
        - Filter by Branch, Journal, Account, Partner, Currency.
        - Export to PDF & Excel.
        - Detailed transactions and balances.
    """,
    'author': 'EMAD Kadry - Taknia Soft',
    'website': 'https://takniasoft.com',
    'category': 'Accounting/Reporting',
    'depends': ['base', 'account', 'branch'],
    'data': [
        'security/ir.model.access.csv',
        'views/branch_accounting_report_wizard_view.xml',
        'views/partner_ledger_report_wizard_view.xml',
        'reports/branch_accounting_report.xml',
        'reports/partner_ledger_report.xml',
    ],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
