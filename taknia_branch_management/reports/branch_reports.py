from odoo import models

class BranchReport(models.AbstractModel):
    _name = 'report.taknia_branch_management.branch_report'
    _description = 'Branch Performance Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['taknia.branch'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'taknia.branch',
            'docs': docs,
        }