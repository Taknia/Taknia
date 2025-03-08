from odoo import models, fields, api

class BranchScoring(models.Model):
    _name = 'branch.scoring'
    _description = 'Branch Scoring'

    branch_id = fields.Many2one('branch.management', string='Branch', required=True)
    score = fields.Float(string='Score')
    date = fields.Date(string='Date', default=fields.Date.today)
    # Add additional fields and methods as necessary