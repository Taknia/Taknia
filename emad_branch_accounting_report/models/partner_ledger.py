from odoo import models, fields, api

class PartnerLedgerReport(models.TransientModel):
    _name = 'partner.ledger.report'
    _description = 'Partner Ledger Report'

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    branch_id = fields.Many2one('res.branch', string='Branch')
    partner_id = fields.Many2one('res.partner', string='Partner')
    journal_ids = fields.Many2many('account.journal', string='Journals')
    account_ids = fields.Many2many('account.account', string='Accounts')
    currency_id = fields.Many2one('res.currency', string='Currency')

    def action_print_report(self):
        data = {
            'form': self.read()[0]
        }
        return self.env.ref('emad_branch_accounting_report.action_print_partner_ledger_report').report_action(self, data=data)
