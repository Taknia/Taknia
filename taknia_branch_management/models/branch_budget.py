from odoo import models, fields

class BranchBudget(models.Model):
    _name = 'taknia.branch.budget'
    _description = 'Branch Budget'

    branch_id = fields.Many2one('taknia.branch', string='Branch', required=True)
    fiscal_year = fields.Char(string='Fiscal Year', required=True)
    allocated_budget = fields.Float(string='Allocated Budget', required=True)
    spent_budget = fields.Float(string='Spent Budget', required=True)
    remaining_budget = fields.Float(string='Remaining Budget', compute='_compute_remaining_budget', store=True)

    @api.depends('allocated_budget', 'spent_budget')
    def _compute_remaining_budget(self):
        for record in self:
            record.remaining_budget = record.allocated_budget - record.spent_budget