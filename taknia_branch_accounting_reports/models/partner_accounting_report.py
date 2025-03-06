from odoo import models, fields

class PartnerAccountingReport(models.TransientModel):
    _name = 'partner.accounting.report'
    _description = 'Partner Accounting Report'

    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    branch_id = fields.Many2one('res.branch', string="Branch")
    account_ids = fields.Many2many('account.account', string="Accounts")
    partner_ids = fields.Many2many('res.partner', string="Partners")
    journal_ids = fields.Many2many('account.journal', string="Journals")
    currency_id = fields.Many2one('res.currency', string="Currency")

    def generate_pdf_report(self):
        return self.env.ref('taknia_branch_accounting_reports.action_partner_accounting_report_pdf').report_action(self)

    def generate_xlsx_report(self):
        return self.env.ref('taknia_branch_accounting_reports.action_partner_accounting_report_xlsx').report_action(self)
