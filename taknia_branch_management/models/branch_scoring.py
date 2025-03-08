from odoo import models, fields

class BranchScoring(models.Model):
    _name = 'branch.scoring'
    _description = 'Branch Scoring'

    branch_id = fields.Many2one('branch', 'Branch', required=True)
    score = fields.Float('Score')
    date = fields.Date('Date', required=True)