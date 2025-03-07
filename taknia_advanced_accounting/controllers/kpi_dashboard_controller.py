from odoo import http
from odoo.http import request
import random

class KpiDashboardController(http.Controller):

    @http.route('/taknia_advanced_accounting/get_kpi_data', type='json', auth='user')
    def get_kpi_data(self):
        """توفير بيانات للـ KPI charts في الصفحة."""

        labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        # بيانات افتراضية - تقدر تربطها بالـ models الفعلية بعدين
        revenue_data = [random.randint(10000, 50000) for _ in labels]
        profit_margin_data = [random.uniform(10, 30) for _ in labels]
        customer_growth_data = [random.randint(50, 200) for _ in labels]

        data = {
            'revenue': {
                'labels': labels,
                'values': revenue_data
            },
            'profit_margin': {
                'labels': labels,
                'values': profit_margin_data
            },
            'customer_growth': {
                'labels': labels,
                'values': customer_growth_data
            },
        }

        return data
