{
    'name': 'Taknia Branch Management',
    'version': '18.0.1.0.0',
    'category': 'Operations/Branches',
    'summary': 'Professional Branch Management System',
    'description': """
Taknia Branch Management
=======================
Professional branch management system with advanced features:

Key Features:
------------
* Multi-branch & Multi-company support
* Advanced reporting and analytics
* Branch performance tracking
* Customer analysis
* Budget management
* ESG reporting
* AI-powered insights
* Regional management
* Google Sheets & Power BI integration

Technical Features:
-----------------
* Mobile-responsive
* Dark mode support
* Advanced security roles
* PDF & Excel exports
* REST API integration
* Real-time analytics
    """,
    'author': 'Taknia',
    'website': 'https://www.example.com',
    'depends': [
        'base',
        'mail',
        'account',
        'stock',
        'hr',
        'web',
        'board',
        'report_xlsx'
    ],
    'data': [
        # Security
        'security/branch_security.xml',
        'security/ir.model.access.csv',

        # Data
        'data/branch_sequence.xml',
        'data/branch_data.xml',

        # Views
        'views/branch_views.xml',
        'views/branch_dashboard.xml',
        'views/branch_settings.xml',
        'views/branch_analysis_views.xml',
        'views/branch_customer_views.xml',
        'views/branch_employee_views.xml',
        'views/branch_budget_views.xml',
        'views/branch_esg_views.xml',
        'views/menu_views.xml',

        # Reports
        'reports/branch_reports.xml',
        'reports/financial_reports.xml',
        'reports/customer_reports.xml',
        'reports/employee_reports.xml',
        'reports/inventory_reports.xml',
        'reports/esg_reports.xml',
        'reports/performance_reports.xml',

        # Wizards
        'wizards/branch_analysis_wizard_views.xml',
        'wizards/report_wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'taknia_branch_management/static/src/scss/style.scss',
            'taknia_branch_management/static/src/js/dashboard.js',
            'taknia_branch_management/static/src/js/charts.js',
            'taknia_branch_management/static/src/js/ai_advisor.js',
        ],
        'web.assets_qweb': [
            'taknia_branch_management/static/src/xml/dashboard_templates.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/description/icon.png'],
}