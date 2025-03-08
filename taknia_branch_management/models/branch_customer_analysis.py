from odoo import models, fields

class BranchCustomerAnalysis(models.Model):
    _name = 'branch.customer.analysis'
    _description = 'Branch Customer Analysis'

    branch_id = fields.Many2one('branch', 'Branch', required=True)
    customer_segment = fields.Char('Customer Segment', required=True)
    analysis_data = fields.Text('Analysis Data')
    date = fields.Date('Date', required=True)