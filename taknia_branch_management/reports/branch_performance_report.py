from odoo import models

class BranchPerformanceReport(models.AbstractModel):
    _name = 'report.taknia_branch_management.branch_performance_report'
    _description = 'Branch Performance Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['taknia.branch.performance'].browse(docids)
        return {
            'docs': docs,
        }