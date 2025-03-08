from odoo import models, fields

class BankIntegration(models.Model):
    _name = 'bank.integration'
    _description = 'Bank Integration'

    branch_id = fields.Many2one('branch', 'Branch', required=True)
    integration_status = fields.Selection([('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')], 'Integration Status')
    last_integration_date = fields.Date('Last Integration Date')