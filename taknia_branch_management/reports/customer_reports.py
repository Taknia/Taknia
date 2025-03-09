from odoo import models

class CustomerReport(models.AbstractModel):
    _name = 'report.taknia_branch_management.customer_report'
    _description = 'Customer Analysis Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['taknia.customer.analysis'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'taknia.customer.analysis',
            'docs': docs,
        }