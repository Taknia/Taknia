import gspread
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from google.oauth2.service_account import Credentials
import logging

_logger = logging.getLogger(__name__)

class GoogleSheetsSync(models.Model):
    _name = 'taknia.google.sheets.sync'
    _description = 'Google Sheets Synchronization - Financial Reports'
    
    name = fields.Char(string="Sheet Name", required=True)
    spreadsheet_id = fields.Char(string="Spreadsheet ID", required=True)
    last_sync_date = fields.Datetime(string="Last Sync Date")
    sheet_url = fields.Char(string="Sheet URL", compute='_compute_sheet_url', store=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)

    @api.depends('spreadsheet_id')
    def _compute_sheet_url(self):
        for record in self:
            if record.spreadsheet_id:
                record.sheet_url = f"https://docs.google.com/spreadsheets/d/{record.spreadsheet_id}"
            else:
                record.sheet_url = ''

    def action_sync_to_google_sheets(self):
        """نقل البيانات المحاسبية (على سبيل المثال: أرصدة الحسابات) إلى Google Sheets"""
        for record in self:
            try:
                credentials = self._get_google_credentials()
                gc = gspread.authorize(credentials)

                spreadsheet = gc.open_by_key(record.spreadsheet_id)
                sheet = spreadsheet.sheet1

                data = self._prepare_financial_data()

                # Clear and update
                sheet.clear()
                sheet.update('A1', data)

                record.write({'last_sync_date': fields.Datetime.now()})
                _logger.info(f"Successfully synced data to Google Sheet: {record.spreadsheet_id}")
            except Exception as e:
                raise UserError(_("Failed to sync data to Google Sheets: %s") % str(e))

    def _prepare_financial_data(self):
        """تجهيز بيانات التقرير المالي لنقلها إلى Google Sheets"""
        data = [
            ['Account', 'Balance'],
        ]
        accounts = self.env['account.account'].search([])
        for account in accounts:
            balance = sum(account.move_line_ids.filtered(lambda l: l.date <= fields.Date.today()).mapped('balance'))
            data.append([account.name, balance])
        return data

    def _get_google_credentials(self):
        """تحميل بيانات الخدمة من ملف الإعدادات أو قاعدة البيانات"""
        google_credentials = self.env['ir.config_parameter'].sudo().get_param('taknia_google_credentials_json', '')
        if not google_credentials:
            raise UserError(_('Google Service Account credentials not found. Please configure them.'))

        import json
        credentials_info = json.loads(google_credentials)

        return Credentials.from_service_account_info(
            credentials_info,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
