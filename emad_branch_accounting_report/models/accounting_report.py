from odoo import models, fields, api

class AccountingReport(models.TransientModel):
    _name = 'accounting.report'
    _description = 'Accounting Report'

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    branch_id = fields.Many2one('res.branch', string='Branch')
    partner_id = fields.Many2one('res.partner', string='Partner')
    journal_ids = fields.Many2many('account.journal', string='Journals')
    account_ids = fields.Many2many('account.account', string='Accounts')
    currency_id = fields.Many2one('res.currency', string='Currency')
    report_type = fields.Selection([
        ('balance', 'Trial Balance'),
        ('ledger', 'Detailed Ledger'),
        ('journal', 'Journal Entries')
    ], string='Report Type', required=True, default='balance')

    def action_print_report(self):
        data = {
            'form': self.read()[0]
        }
        return self.env.ref('emad_branch_accounting_report.action_print_accounting_report').report_action(self, data=data)
