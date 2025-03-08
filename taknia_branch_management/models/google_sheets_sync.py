from odoo import models, fields, api

class GoogleSheetsSync(models.Model):
    _name = 'google.sheets.sync'
    _description = 'Google Sheets Sync'

    branch_id = fields.Many2one('branch.management', string='Branch', required=True)
    sheet_url = fields.Char(string='Google Sheet URL')
    last_sync_date = fields.Date(string='Last Sync Date')
    # Add additional fields and methods as necessary