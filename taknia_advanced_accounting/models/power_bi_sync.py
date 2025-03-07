import requests
import json
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PowerBISync(models.Model):
    _name = 'power.bi.sync'
    _description = 'Power BI Data Sync'
    
    name = fields.Char(string="Sync Name", default="Power BI Sync", readonly=True)
    last_sync_date = fields.Datetime(string="Last Sync Date")
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], string="Sync Status", default='draft')

    def sync_with_power_bi(self):
        """ Main function to trigger data sync with Power BI """
        self.ensure_one()
        self.write({'status': 'in_progress'})

        try:
            # Get credentials from system parameters
            client_id = self.env['ir.config_parameter'].sudo().get_param('taknia_advanced_accounting.powerbi_client_id')
            client_secret = self.env['ir.config_parameter'].sudo().get_param('taknia_advanced_accounting.powerbi_client_secret')
            tenant_id = self.env['ir.config_parameter'].sudo().get_param('taknia_advanced_accounting.powerbi_tenant_id')

            if not client_id or not client_secret or not tenant_id:
                raise UserError(_("Power BI credentials are missing. Please check the system settings."))

            # Get Access Token
            token = self._get_power_bi_access_token(client_id, client_secret, tenant_id)

            # Prepare financial data (Example: Trial Balance Summary)
            financial_data = self._prepare_financial_data()

            # Send data to Power BI (replace with your actual Power BI Dataset URL)
            self._send_data_to_power_bi(token, financial_data)

            self.write({
                'last_sync_date': fields.Datetime.now(),
                'status': 'completed'
            })
        except Exception as e:
            self.write({'status': 'failed'})
            raise UserError(_("Failed to sync with Power BI: %s") % str(e))

    def _get_power_bi_access_token(self, client_id, client_secret, tenant_id):
        """ Get OAuth2 token for Power BI """
        url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        data = {
            'client_id': client_id,
            'scope': 'https://graph.microsoft.com/.default',
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
        }
        response = requests.post(url, data=data)

        if response.status_code != 200:
            raise UserError(_("Failed to authenticate with Power BI. Check credentials."))

        return response.json().get('access_token')

    def _prepare_financial_data(self):
        """ Example: Prepare sample financial data (can be extended) """
        accounts = self.env['account.account'].search([])
        data = []
        for account in accounts:
            data.append({
                'account_code': account.code,
                'account_name': account.name,
                'balance': account.balance,
            })
        return data

    def _send_data_to_power_bi(self, token, data):
        """ Send data to Power BI (You need to replace with actual Power BI Push URL) """
        dataset_url = 'https://api.powerbi.com/v1.0/myorg/datasets/YOUR_DATASET_ID/rows'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        payload = json.dumps(data)

        response = requests.post(dataset_url, headers=headers, data=payload)

        if response.status_code not in [200, 201]:
            raise UserError(_("Failed to send data to Power BI: %s") % response.text)

