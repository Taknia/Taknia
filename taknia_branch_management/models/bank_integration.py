from odoo import models, fields, api

class BankIntegration(models.Model):
    _name = 'bank.integration'
    _description = 'Bank Integration'

    branch_id = fields.Many2one('branch.management', string='Branch', required=True)
    bank_name = fields.Char(string='Bank Name', required=True)
    account_number = fields.Char(string='Account Number', required=True)
    last_sync_date = fields.Date(string='Last Sync Date')
    # Add additional fields and methods as necessary