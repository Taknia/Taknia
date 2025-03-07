from odoo import models, fields, api

class FinancialReportWizard(models.TransientModel):
    _name = 'financial.report.wizard'
    _description = 'Financial Report Wizard'

    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    branch_id = fields.Many2one('res.branch', string='Branch')
    account_ids = fields.Many2many('account.account', string='Accounts')
    partner_ids = fields.Many2many('res.partner', string='Partners')
    journal_ids = fields.Many2many('account.journal', string='Journals')
    currency_id = fields.Many2one('res.currency', string='Currency')
    report_type = fields.Selection([
        ('balance', 'Balance Sheet'),
        ('pnl', 'Profit & Loss'),
        ('trial', 'Trial Balance'),
    ], string='Report Type', required=True)

    def action_print_report(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'branch_id': self.branch_id.id if self.branch_id else False,
            'account_ids': self.account_ids.ids,
            'partner_ids': self.partner_ids.ids,
            'journal_ids': self.journal_ids.ids,
            'currency_id': self.currency_id.id if self.currency_id else False,
            'report_type': self.report_type,
        }
        return self.env.ref('taknia_advanced_accounting.action_financial_report').report_action(None, data=data)

