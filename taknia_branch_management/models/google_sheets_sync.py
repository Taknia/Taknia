from odoo import models, fields

class GoogleSheetsSync(models.Model):
    _name = 'google.sheets.sync'
    _description = 'Google Sheets Sync'

    branch_id = fields.Many2one('branch', 'Branch', required=True)
    sheet_url = fields.Char('Sheet URL')
    sync_status = fields.Selection([('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')], 'Sync Status')
    last_sync_date = fields.Date('Last Sync Date')