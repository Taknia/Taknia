from odoo import models, fields

class BranchFinancialHealth(models.Model):
    _name = 'branch.financial.health'
    _description = 'Branch Financial Health'

    branch_id = fields.Many2one('branch', 'Branch', required=True)
    financial_metric = fields.Char('Financial Metric', required=True)
    value = fields.Float('Value')
    date = fields.Date('Date', required=True)