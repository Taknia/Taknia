from odoo import models, fields, api

class BranchBudget(models.Model):
    _name = 'branch.budget'
    _description = 'Branch Budget'

    branch_id = fields.Many2one('branch.management', string='Branch', required=True)
    fiscal_year = fields.Char(string='Fiscal Year', required=True)
    budget_amount = fields.Float(string='Budget Amount')
    spent_amount = fields.Float(string='Spent Amount')
    remaining_amount = fields.Float(string='Remaining Amount', compute='_compute_remaining_amount')

    @api.depends('budget_amount', 'spent_amount')
    def _compute_remaining_amount(self):
        for record in self:
            record.remaining_amount = record.budget_amount - record.spent_amount
    # Add additional fields and methods as necessary