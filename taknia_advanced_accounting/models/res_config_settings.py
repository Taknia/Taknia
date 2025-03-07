from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # ChatGPT API
    chatgpt_api_key = fields.Char(string="ChatGPT API Key")

    # Google Sheets
    google_sheets_credentials = fields.Text(string="Google Sheets Credentials (JSON)")

    # Power BI
    powerbi_client_id = fields.Char(string="Power BI Client ID")
    powerbi_client_secret = fields.Char(string="Power BI Client Secret")
    powerbi_tenant_id = fields.Char(string="Power BI Tenant ID")

    # Bank Integration
    bank_api_url = fields.Char(string="Bank API URL")
    bank_api_key = fields.Char(string="Bank API Key")

    def set_values(self):
        super(ResConfigSettings, self).set_values()

        self.env['ir.config_parameter'].sudo().set_param('taknia_advanced_accounting.chatgpt_api_key', self.chatgpt_api_key)
        self.env['ir.config_parameter'].sudo().set_param('taknia_advanced_accounting.google_sheets_credentials', self.google_sheets_credentials)
        self.env['ir.config_parameter'].sudo().set_param('taknia_advanced_accounting.powerbi_client_id', self.powerbi_client_id)
        self.env['ir.config_parameter'].sudo().set_param('taknia_advanced_accounting.powerbi_client_secret', self.powerbi_client_secret)
        self.env['ir.config_parameter'].sudo().set_param('taknia_advanced_accounting.powerbi_tenant_id', self.powerbi_tenant_id)
        self.env['ir.config_parameter'].sudo().set_param('taknia_advanced_accounting.bank_api_url', self.bank_api_url)
        self.env['ir.config_parameter'].sudo().set_param('taknia_advanced_accounting.bank_api_key', self.bank_api_key)

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()

        res.update(
            chatgpt_api_key=self.env['ir.config_parameter'].sudo().get_param('taknia_advanced_accounting.chatgpt_api_key', default=''),
            google_sheets_credentials=self.env['ir.config_parameter'].sudo().get_param('taknia_advanced_accounting.google_sheets_credentials', default=''),
            powerbi_client_id=self.env['ir.config_parameter'].sudo().get_param('taknia_advanced_accounting.powerbi_client_id', default=''),
            powerbi_client_secret=self.env['ir.config_parameter'].sudo().get_param('taknia_advanced_accounting.powerbi_client_secret', default=''),
            powerbi_tenant_id=self.env['ir.config_parameter'].sudo().get_param('taknia_advanced_accounting.powerbi_tenant_id', default=''),
            bank_api_url=self.env['ir.config_parameter'].sudo().get_param('taknia_advanced_accounting.bank_api_url', default=''),
            bank_api_key=self.env['ir.config_parameter'].sudo().get_param('taknia_advanced_accounting.bank_api_key', default=''),
        )
        return res
