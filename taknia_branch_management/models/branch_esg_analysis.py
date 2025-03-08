from odoo import models, fields

class BranchESGAnalysis(models.Model):
    _name = 'branch.esg.analysis'
    _description = 'Branch ESG Analysis'

    branch_id = fields.Many2one('branch', 'Branch', required=True)
    esg_metric = fields.Char('ESG Metric', required=True)
    value = fields.Float('Value')
    date = fields.Date('Date', required=True)