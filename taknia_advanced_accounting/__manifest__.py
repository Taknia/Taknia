{
    'name': 'Taknia Advanced Accounting',
    'version': '1.0',
    'summary': 'Advanced Accounting Management with AI, KPIs, Branch Analysis & Financial Intelligence',
    'sequence': 10,
    'author': 'Emad Kadry - Taknia Soft',
    'website': 'http://www.takniasoft.com',
    'category': 'Accounting/Advanced',
    'license': 'LGPL-3',
    'depends': ['account', 'base', 'taknia_branch_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/menus.xml',

        # Views
        'views/financial_report_views.xml',
        'views/ai_recommendation_views.xml',
        'views/kpi_dashboard_views.xml',
        'views/customer_scoring_views.xml',
        'views/product_analysis_views.xml',
        'views/esg_analysis_views.xml',
        'views/partner_profitability_views.xml',
        'views/branch_comparison_views.xml',
        'views/res_config_settings_view.xml'

        # Wizards (شاشات الخيارات للتقارير والتوصيات)
        'wizards/accounting_report_wizard.xml',
        'wizards/partner_ledger_wizard.xml',
        'wizards/financial_advice_wizard.xml',

        # Reports Actions (ربط التقارير)
        'reports/financial_report_actions.xml',
        'reports/ai_recommendation_actions.xml',
        'reports/monthly_report_actions.xml',

        # Reports Templates (تصاميم PDF)
        'reports/report_templates/financial_report_template.xml',
        'reports/report_templates/ai_recommendation_template.xml',
        'reports/report_templates/monthly_report_template.xml',
        'reports/report_templates/partner_ledger_report_template.xml',

        # Cron Jobs (مهام مجدولة)
        'data/cron_jobs.xml',

        # Settings (لوحة الإعدادات)
        'views/module_settings_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'taknia_advanced_accounting/static/src/css/custom_styles.css',
            'taknia_advanced_accounting/static/src/js/kpi_charts.js',
        ],
    },
    'application': True,
    'installable': True,
    'auto_install': False,
    'description': """
        Taknia Advanced Accounting by Emad Kadry
        -----------------------------------------
        - Comprehensive accounting reports with AI-driven financial insights.
        - Full integration with Google Sheets & Power BI.
        - Advanced financial KPIs and profitability analysis.
        - Predictive analytics, ESG analysis, and multi-branch support.
        - Direct integration with banks & payment gateways.
        - Financial health score and intelligent recommendations.
    """,
    'images': ['static/description/icon.png'],
    'support': 'support@takniasoft.com',
    'maintainer': 'Emad Kadry'
}
