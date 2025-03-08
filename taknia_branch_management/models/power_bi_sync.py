from odoo import models, fields

class PowerBISync(models.Model):
    _name = 'power.bi.sync'
    _description = 'Power BI Sync'

    branch_id = fields.Many2one('branch', 'Branch', required=True)
    report_url = fields.Char('Report URL')
    sync_status = fields.Selection([('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')], 'Sync Status')
    last_sync_date = fields.Date('Last Sync Date')