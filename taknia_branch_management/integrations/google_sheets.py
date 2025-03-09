from odoo import models, fields, api
import gspread
from oauth2client.service_account import ServiceAccountCredentials

class GoogleSheetsIntegration(models.Model):
    _name = 'taknia.google.sheets'
    _description = 'Google Sheets Integration'

    name = fields.Char(string='Sheet Name', required=True)
    sheet_id = fields.Char(string='Sheet ID', required=True)

    def export_branch_data(self):
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('/path/to/credentials.json', scope)
        client = gspread.authorize(creds)

        sheet = client.open_by_key(self.sheet_id).sheet1
        branches = self.env['taknia.branch'].search([])

        data = [["Branch Name", "Code", "Manager", "Region", "Budget", "Revenue", "Expenses"]]
        for branch in branches:
            data.append([branch.name, branch.code, branch.manager_id.name, branch.region, branch.budget, branch.revenue, branch.expenses])

        sheet.update(data)