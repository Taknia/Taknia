from odoo import models, fields, api, _

class PartnerLedgerReportWizard(models.TransientModel):
    _name = 'partner.ledger.report.wizard'
    _description = 'Partner Ledger Report Wizard'

    date_from = fields.Date(string='Start Date', required=True)
    date_to = fields.Date(string='End Date', required=True)
    branch_ids = fields.Many2many('res.branch', string='Branches')
    partner_ids = fields.Many2many('res.partner', string='Partners')
    account_ids = fields.Many2many('account.account', string='Accounts')
    journal_ids = fields.Many2many('account.journal', string='Journals')
    currency_id = fields.Many2one('res.currency', string='Currency', help="Choose currency to filter entries.")

    target_move = fields.Selection([
        ('all', 'All Entries'),
        ('posted', 'Posted Entries'),
    ], string='Target Moves', default='posted', required=True)

    def action_print_pdf(self):
        return self._generate_report('pdf')

    def action_print_excel(self):
        return self._generate_report('xlsx')

    def _generate_report(self, report_type):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'branch_ids': self.branch_ids.ids,
            'partner_ids': self.partner_ids.ids,
            'account_ids': self.account_ids.ids,
            'journal_ids': self.journal_ids.ids,
            'currency_id': self.currency_id.id,
            'target_move': self.target_move,
        }
        return self.env.ref(f'emad_branch_accounting_report.partner_ledger_report_{report_type}_action').report_action(self, data=data)
