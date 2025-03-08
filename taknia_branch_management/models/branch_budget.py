from odoo import models, fields

class BranchBudget(models.Model):
    _name = 'branch.budget'
    _description = 'Branch Budget'

    branch_id = fields.Many2one('branch', 'Branch', required=True)
    fiscal_year = fields.Char('Fiscal Year', required=True)
    budget_amount = fields.Float('Budget Amount')
    actual_amount = fields.Float('Actual Amount')
    variance = fields.Float('Variance', compute='_compute_variance')

    def _compute_variance(self):
        for record in self:
            record.variance = record.budget_amount - record.actual_amount