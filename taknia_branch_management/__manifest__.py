{
    'name': 'Taknia Branch Management',
    'version': '1.0',
    'summary': 'إدارة الفروع المتقدمة مع ذكاء صناعي ولوحات تحكم وتقارير تحليلية',
    'description': """
    موديول Taknia Branch Management لإدارة الفروع بشكل احترافي يشمل:
    - تعريف الفروع وربطها بالعملاء والموظفين والمخزون والمصاريف.
    - لوحات تحكم متقدمة.
    - تقارير تحليلية مقارنة بين الفروع.
    - ذكاء صناعي يقترح استشارات مالية.
    - تكامل مع Google Sheets و Power BI.
    - تقارير PDF وExcel قابلة للتخصيص.
    - دعم Multi-Company و Multi-Branch.
    - إعدادات متقدمة مع صلاحيات لكل فرع.
    """,
    'author': 'Taknia Soft - Emad Kadry',
    'website': 'https://www.takniasoft.com',
    'category': 'Taknia Modules',
    'depends': ['base', 'account', 'hr', 'stock', 'taknia_advanced_accounting'],
    'data': [
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/branch_views.xml',
        'views/branch_performance_views.xml',
        'views/branch_budget_views.xml',
        'views/kpi_dashboard_views.xml',
        'views/ai_branch_advisor_views.xml',
        'views/branch_customer_analysis_views.xml',
        'views/branch_expense_analysis_views.xml',
        'views/branch_stock_analysis_views.xml',
        'views/branch_employee_analysis_views.xml',
        'views/branch_esg_analysis_views.xml',
        'views/branch_financial_health_views.xml',
        'views/branch_scoring_views.xml',
        'views/regional_management_views.xml',
        'views/module_settings_views.xml',
        'reports/report_templates/branch_performance_template.xml',
        'reports/report_templates/branch_financial_health_template.xml',
        'reports/report_templates/branch_expense_analysis_template.xml',
        'reports/report_templates/branch_stock_analysis_template.xml',
        'reports/report_templates/branch_customer_analysis_template.xml',
        'reports/report_templates/branch_scoring_template.xml',
        'reports/report_templates/regional_comparison_template.xml',
        'reports/report_templates/ai_recommendation_template.xml',
        'reports/report_actions/branch_performance_actions.xml',
        'reports/report_actions/branch_financial_health_actions.xml',
        'reports/report_actions/branch_expense_analysis_actions.xml',
        'reports/report_actions/branch_stock_analysis_actions.xml',
        'reports/report_actions/branch_customer_analysis_actions.xml',
        'reports/report_actions/branch_scoring_actions.xml',
        'reports/report_actions/regional_comparison_actions.xml',
        'reports/report_actions/ai_recommendation_actions.xml',
        'wizards/branch_performance_wizard.xml',
        'wizards/financial_advice_wizard.xml',
        'data/cron_jobs.xml',
        'static/src/css/custom_styles.css',
        'static/src/js/kpi_charts.js',
    ],
    'assets': {
        'web.assets_backend': [
            'taknia_branch_management/static/src/css/custom_styles.css',
            'taknia_branch_management/static/src/js/kpi_charts.js',
        ],
    },
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
    'auto_install': False,
}
