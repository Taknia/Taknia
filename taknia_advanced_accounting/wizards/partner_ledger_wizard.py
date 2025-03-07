from odoo import models, fields, api
from odoo.exceptions import UserError
import io
import base64
from datetime import datetime

class PartnerLedgerWizard(models.TransientModel):
    _name = 'partner.ledger.wizard'
    _description = 'Partner Ledger Report Wizard'

    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    branch_id = fields.Many2one('res.branch', string='Branch')
    partner_ids = fields.Many2many('res.partner', string='Partners')
    account_ids = fields.Many2many('account.account', string='Accounts')
    journal_ids = fields.Many2many('account.journal', string='Journals')
    currency_id = fields.Many2one('res.currency', string='Currency')
    show_details = fields.Boolean(string='Show Details', default=True)
    output_format = fields.Selection([
        ('pdf', 'PDF'),
        ('xlsx', 'Excel')
    ], string='Output Format', default='pdf')

    def action_generate_partner_ledger(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'branch_id': self.branch_id.id,
            'partner_ids': self.partner_ids.ids,
            'account_ids': self.account_ids.ids,
            'journal_ids': self.journal_ids.ids,
            'currency_id': self.currency_id.id,
            'show_details': self.show_details,
            'output_format': self.output_format,
        }

        if self.output_format == 'pdf':
            return self.env.ref('taknia_advanced_accounting.partner_ledger_pdf_report').report_action(self, data=data)
        elif self.output_format == 'xlsx':
            return self.generate_excel_report(data)

    def generate_excel_report(self, data):
        report_data = self._fetch_report_data(data)

        output = io.BytesIO()
        workbook = self.env['report.taknia_advanced_accounting.report_helper'].create_xlsx_partner_ledger(workbook=None, data=report_data)

        workbook.save(output)
        output.seek(0)

        attachment = self.env['ir.attachment'].create({
            'name': f'Partner Ledger {self.date_from} - {self.date_to}.xlsx',
            'type': 'binary',
            'datas': base64.b64encode(output.read()),
            'res_model': 'partner.ledger.wizard',
            'res_id': self.id,
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

    def _fetch_report_data(self, data):
        domain = [('date', '>=', data['date_from']), ('date', '<=', data['date_to'])]

        if data['branch_id']:
            domain.append(('branch_id', '=', data['branch_id']))

        if data['partner_ids']:
            domain.append(('partner_id', 'in', data['partner_ids']))

        if data['account_ids']:
            domain.append(('account_id', 'in', data['account_ids']))

        if data['journal_ids']:
            domain.append(('journal_id', 'in', data['journal_ids']))

        moves = self.env['account.move.line'].search(domain)

        report_data = {}
        for line in moves:
            partner = line.partner_id
            if partner not in report_data:
                report_data[partner] = {
                    'lines': [],
                    'debit': 0,
                    'credit': 0,
                    'balance': 0,
                }
            report_data[partner]['lines'].append(line)
            report_data[partner]['debit'] += line.debit
            report_data[partner]['credit'] += line.credit
            report_data[partner]['balance'] += (line.debit - line.credit)

        return report_data
