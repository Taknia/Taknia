import io
import xlsxwriter
from odoo import models
from odoo.http import request

class BranchReportExcel(models.AbstractModel):
    _name = 'report.taknia_branch_management.branch_report_excel'
    _description = 'Branch Performance Report (Excel)'

    def _get_report_values(self, docids, data=None):
        return {'docs': self.env['taknia.branch'].browse(docids)}

    def generate_xlsx_report(self, workbook, data, branches):
        sheet = workbook.add_worksheet('Branches Report')
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, 'Branch Name', bold)
        sheet.write(0, 1, 'Revenue', bold)
        sheet.write(0, 2, 'Expenses', bold)
        
        row = 1
        for branch in branches:
            sheet.write(row, 0, branch.name)
            sheet.write(row, 1, branch.revenue)
            sheet.write(row, 2, branch.expenses)
            row += 1

class BranchReportPDF(models.AbstractModel):
    _name = 'report.taknia_branch_management.branch_report_pdf'
    _description = 'Branch Performance Report (PDF)'

    def _get_report_values(self, docids, data=None):
        return {'docs': self.env['taknia.branch'].browse(docids)}