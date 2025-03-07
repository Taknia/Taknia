from odoo import models, fields, api

class BranchComparisonWizard(models.TransientModel):
    _name = 'branch.comparison.wizard'
    _description = 'Branch Comparison Wizard'

    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    branch_ids = fields.Many2many('res.branch', string='Branches', required=True)

    def action_compare_branches(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'branch_ids': self.branch_ids.ids,
        }
        return self.env.ref('taknia_advanced_accounting.action_branch_comparison_report').report_action(None, data=data)
