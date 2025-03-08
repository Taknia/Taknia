from odoo import models, fields

class BranchPerformance(models.Model):
    _name = 'branch.performance'
    _description = 'Branch Performance'

    branch_id = fields.Many2one('branch', 'Branch', required=True)
    date = fields.Date('Date', required=True)
    revenue = fields.Float('Revenue')
    expenses = fields.Float('Expenses')
    profit = fields.Float('Profit', compute='_compute_profit')

    def _compute_profit(self):
        for record in self:
            record.profit = record.revenue - record.expenses