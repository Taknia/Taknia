from odoo import models, fields

class TakniaAdvancedSettings(models.Model):
    _name = 'taknia.advanced.settings'
    _description = 'Advanced System Settings'

    enable_dark_mode = fields.Boolean(string='Enable Dark Mode', default=False)
    enable_google_sheets = fields.Boolean(string='Enable Google Sheets Integration', default=True)
    enable_power_bi = fields.Boolean(string='Enable Power BI Integration', default=True)
    enable_bank_integration = fields.Boolean(string='Enable Bank Integration', default=False)