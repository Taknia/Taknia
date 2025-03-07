import gspread
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from oauth2client.service_account import ServiceAccountCredentials
import json
import base64


class BranchGoogleSheetsSync(models.Model):
    _name = 'branch.google.sheets.sync'
    _description = 'Google Sheets Synchronization for Branches'

    name = fields.Char(string="Sync Name", required=True, default="Google Sheets Sync")
    spreadsheet_url = fields.Char(string="Spreadsheet URL", readonly=True)
    sync_status = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('success', 'Success'),
        ('failed', 'Failed')
    ], string="Sync Status", default='pending', readonly=True)
    
    branch_ids = fields.Many2many('res.branch', string="Branches to Sync")
    last_sync_date = fields.Datetime(string="Last Sync Date", readonly=True)
    
    google_credentials = fields.Binary(string="Google API Credentials (JSON)")
    google_credentials_filename = fields.Char(string="Credentials Filename")

    # ----------------------------------------
    # تحميل بيانات Google Sheets API
    # ----------------------------------------
    def get_google_sheets_client(self):
        if not self.google_credentials:
            raise UserError(_("Please upload your Google API credentials JSON file."))

        credentials_content = base64.b64decode(self.google_credentials)
        credentials_dict = json.loads(credentials_content.decode('utf-8'))

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
        return gspread.authorize(credentials)

    # ----------------------------------------
    # مزامنة البيانات مع Google Sheets
    # ----------------------------------------
    def action_sync_with_google_sheets(self):
        for record in self:
            record.sync_status = 'in_progress'
            try:
                client = record.get_google_sheets_client()
                
                # إنشاء ملف جديد في Google Sheets
                spreadsheet = client.create(f"Branch Data Sync - {record.name}")
                spreadsheet.share('your-email@gmail.com', perm_type='user', role='writer')  # تحديث الإيميل

                # تحديد ورقة العمل الأولى
                worksheet = spreadsheet.sheet1
                worksheet.update_title("Branch Performance Data")

                # تحديد البيانات التي سيتم رفعها
                headers = ["Branch Name", "Manager", "Total Revenue", "Total Expenses", "Net Profit", "Performance Score"]
                data = [headers]

                for branch in record.branch_ids:
                    data.append([
                        branch.name,
                        branch.manager_id.name if branch.manager_id else "N/A",
                        branch.total_revenue,
                        branch.total_expenses,
                        branch.total_revenue - branch.total_expenses,
                        branch.branch_performance_score
                    ])

                # تحديث القيم في Google Sheets
                worksheet.update('A1', data)

                # حفظ رابط الجدول في السجل
                record.spreadsheet_url = spreadsheet.url
                record.sync_status = 'success'
                record.last_sync_date = fields.Datetime.now()

            except Exception as e:
                record.sync_status = 'failed'
                raise UserError(_("Google Sheets Sync Failed: %s" % str(e)))

    # ----------------------------------------
    # زر فتح جدول Google Sheets
    # ----------------------------------------
    def action_open_google_sheet(self):
        self.ensure_one()
        if not self.spreadsheet_url:
            raise UserError(_("No spreadsheet URL found. Please sync first."))
        return {
            'type': 'ir.actions.act_url',
            'url': self.spreadsheet_url,
            'target': 'new',
        }
