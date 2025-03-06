from odoo import models, api, fields, _
from odoo.exceptions import UserError
import io
import xlsxwriter

class PartnerLedgerReport(models.AbstractModel):
    _name = 'report.emad_branch_accounting_report.partner_ledger_report_template'
    _description = 'Partner Ledger Report'

    def _get_report_values(self, docids, data=None):
        if not data:
            raise UserError(_("No data provided for the report."))

        partners = self.env['res.partner'].browse(data.get('partner_ids', []))
        branches = self.env['res.branch'].browse(data.get('branch_ids', []))
        currency = self.env['res.currency'].browse(data.get('currency_id'))

        domain = [('date', '>=', data['date_from']), ('date', '<=', data['date_to'])]
        if data['target_move'] == 'posted':
            domain.append(('move_id.state', '=', 'posted'))

        if branches:
            domain.append(('branch_id', 'in', branches.ids))
        if partners:
            domain.append(('partner_id', 'in', partners.ids))
        if currency:
            domain.append(('currency_id', '=', currency.id))

        lines = self.env['account.move.line'].search(domain)

        return {
            'doc_ids': docids,
            'doc_model': 'account.move.line',
            'docs': lines,
            'data': data,
            'partners': partners,
            'branches': branches,
            'currency': currency,
        }

    @api.model
    def _get_xlsx_report(self, data):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Partner Ledger Report')

        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, 'Date', bold)
        sheet.write(0, 1, 'Branch', bold)
        sheet.write(0, 2, 'Partner', bold)
        sheet.write(0, 3, 'Account', bold)
        sheet.write(0, 4, 'Debit', bold)
        sheet.write(0, 5, 'Credit', bold)
        sheet.write(0, 6, 'Balance', bold)

        domain = [('date', '>=', data['date_from']), ('date', '<=', data['date_to'])]
        if data['target_move'] == 'posted':
            domain.append(('move_id.state', '=', 'posted'))

        lines = self.env['account.move.line'].search(domain)

        row = 1
        for line in lines:
            sheet.write(row, 0, str(line.date))
            sheet.write(row, 1, line.branch_id.name if line.branch_id else '')
            sheet.write(row, 2, line.partner_id.name if line.partner_id else '')
            sheet.write(row, 3, line.account_id.name)
            sheet.write(row, 4, line.debit)
            sheet.write(row, 5, line.credit)
            sheet.write(row, 6, line.balance)
            row += 1

        workbook.close()
        output.seek(0)
        return output.read()
