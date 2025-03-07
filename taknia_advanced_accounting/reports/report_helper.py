from odoo import models
import xlsxwriter
from io import BytesIO

class ReportHelper(models.AbstractModel):
    _name = 'report.taknia_advanced_accounting.report_helper'
    _description = 'Report Helper for Excel'

    def create_xlsx_partner_ledger(self, workbook=None, data=None):
        output = BytesIO()
        if not workbook:
            workbook = xlsxwriter.Workbook(output)

        sheet = workbook.add_worksheet('Partner Ledger')

        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3'})
        currency_format = workbook.add_format({'num_format': '#,##0.00'})

        headers = ['Partner', 'Date', 'Journal', 'Account', 'Debit', 'Credit', 'Balance']
        for col_num, header in enumerate(headers):
            sheet.write(0, col_num, header, header_format)

        row = 1
        for partner, info in data.items():
            for line in info['lines']:
                sheet.write(row, 0, partner.name or 'Unknown Partner')
                sheet.write(row, 1, str(line.date))
                sheet.write(row, 2, line.journal_id.name)
                sheet.write(row, 3, f"{line.account_id.code} - {line.account_id.name}")
                sheet.write(row, 4, line.debit, currency_format)
                sheet.write(row, 5, line.credit, currency_format)
                sheet.write(row, 6, line.debit - line.credit, currency_format)
                row += 1

            # Partner Total Row
            sheet.write(row, 3, f'Total for {partner.name}', header_format)
            sheet.write(row, 4, info['debit'], currency_format)
            sheet.write(row, 5, info['credit'], currency_format)
            sheet.write(row, 6, info['balance'], currency_format)
            row += 2

        workbook.close()
        output.seek(0)
        return workbook
