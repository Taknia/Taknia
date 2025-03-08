from odoo import models, fields, api

class BranchPerformance(models.Model):
    _name = 'branch.performance'
    _description = 'Branch Performance'

    branch_id = fields.Many2one('branch.management', string='Branch', required=True)
    kpi = fields.Char(string='KPI', required=True)
    value = fields.Float(string='Value')
    date = fields.Date(string='Date', default=fields.Date.today)
    # Add additional fields and methods as necessary