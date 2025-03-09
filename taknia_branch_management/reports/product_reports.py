from odoo import models

class ProductReport(models.AbstractModel):
    _name = 'report.taknia_branch_management.product_report'
    _description = 'Product Sales Analysis Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['taknia.product.analysis'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'taknia.product.analysis',
            'docs': docs,
        }