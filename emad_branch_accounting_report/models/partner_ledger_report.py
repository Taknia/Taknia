from odoo import models, fields, api, _

class PartnerLedgerReport(models.TransientModel):
    _name = 'partner.ledger.report'
    _description = 'Partner Ledger Report'

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

    @api.model
    def get_report_data(self):
        domain = [('date', '>=', self.date_from), ('date', '<=', self.date_to)]

        if self.branch_ids:
            domain.append(('branch_id', 'in', self.branch_ids.ids))

        if self.partner_ids:
            domain.append(('partner_id', 'in', self.partner_ids.ids))

        if self.account_ids:
            domain.append(('account_id', 'in', self.account_ids.ids))

        if self.journal_ids:
            domain.append(('journal_id', 'in', self.journal_ids.ids))

        if self.currency_id:
            domain.append(('currency_id', '=', self.currency_id.id))

        if self.target_move == 'posted':
            domain.append(('move_id.state', '=', 'posted'))

        lines = self.env['account.move.line'].search(domain)
        return lines
