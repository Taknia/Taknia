from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_google_sheets_sync = fields.Boolean('Google Sheets Sync')
    module_power_bi_sync = fields.Boolean('Power BI Sync')