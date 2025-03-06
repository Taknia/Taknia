from odoo import models, fields, api

class PartnerLedgerReportWizard(models.TransientModel):
    _name = 'partner.ledger.report.wizard'
    _description = 'Partner Ledger Report Wizard'

    date_from = fields.Date(string="Date From", required=True)
    date_to = fields.Date(string="Date To", required=True)
    branch_ids = fields.Many2many('company.branch', string="Branches")
    journal_ids = fields.Many2many('account.journal', string="Journals")
    account_ids = fields.Many2many('account.account', string="Accounts")
    partner_ids = fields.Many2many('res.partner', string="Partners", required=True)
    currency_id = fields.Many2one('res.currency', string="Currency")

    target_move = fields.Selection([
        ('all', 'All Entries'),
        ('posted', 'Posted Entries')
    ], string='Target Moves', default='posted', required=True)

    report_date = fields.Datetime(string='Report Date', default=fields.Datetime.now)

    def action_print_report(self):
        self.ensure_one()
        data = {
            'form': self.read()[0]
        }
        return self.env.ref('emad_branch_accounting_report.action_report_partner_ledger').report_action(self, data=data)
