from odoo import models, fields

class BranchAccountingReportWizard(models.TransientModel):
    _name = 'branch.accounting.report.wizard'
    _description = 'Branch Accounting Report Wizard'

    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    branch_id = fields.Many2one('res.branch', string="Branch")
    account_ids = fields.Many2many('account.account', string="Accounts")
    partner_ids = fields.Many2many('res.partner', string="Partners")
    journal_ids = fields.Many2many('account.journal', string="Journals")
    currency_id = fields.Many2one('res.currency', string="Currency")

    def generate_report(self):
        data = {'form': self.read()[0]}
        return self.env.ref('taknia_branch_accounting_reports.action_branch_accounting_report_pdf').report_action(self, data=data)
