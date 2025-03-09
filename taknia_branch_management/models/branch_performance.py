from odoo import models, fields

class BranchPerformance(models.Model):
    _name = 'taknia.branch.performance'
    _description = 'Branch Performance'

    branch_id = fields.Many2one('taknia.branch', string='Branch', required=True)
    performance_score = fields.Float(string='Performance Score')
    customer_satisfaction = fields.Float(string='Customer Satisfaction (%)')
    esg_rating = fields.Float(string='ESG Rating (%)')
    last_updated = fields.Datetime(string='Last Updated', default=fields.Datetime.now)