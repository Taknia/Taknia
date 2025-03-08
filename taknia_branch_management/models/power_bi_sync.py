from odoo import models, fields, api

class PowerBISync(models.Model):
    _name = 'power.bi.sync'
    _description = 'Power BI Sync'

    branch_id = fields.Many2one('branch.management', string='Branch', required=True)
    report_url = fields.Char(string='Power BI Report URL')
    last_sync_date = fields.Date(string='Last Sync Date')
    # Add additional fields and methods as necessary