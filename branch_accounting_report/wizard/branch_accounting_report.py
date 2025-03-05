from odoo import models, fields, api

class BranchAccountingReportWizard(models.TransientModel):
    _name = 'branch.accounting.report.wizard'
    _description = 'Branch Accounting Report Wizard'

    branch_option = fields.Selection([
        ('all', 'All Branches'),
        ('specific', 'Specific Branch')
    ], string="Branch Selection", default='all')

    branch_ids = fields.Many2many('res.branch', string="Branches")
    journal_ids = fields.Many2many('account.journal', string="Journals")
    account_ids = fields.Many2many('account.account', string="Accounts")
    date_from = fields.Date(string="Start Date")
    date_to = fields.Date(string="End Date")

    @api.onchange('branch_option')
    def _onchange_branch_option(self):
        if self.branch_option == 'all':
            self.branch_ids = self.env['res.branch'].search([])
        else:
            self.branch_ids = False

    @api.onchange('branch_ids')
    def _onchange_branch_ids(self):
        if self.branch_ids:
            return {
                'domain': {
                    'journal_ids': [('branch_id', 'in', self.branch_ids.ids)],
                    'account_ids': [('branch_id', 'in', self.branch_ids.ids)]
                }
            }
        else:
            return {'domain': {'journal_ids': [], 'account_ids': []}}

    def action_print_report(self):
        data = {
            'branch_option': self.branch_option,
            'branches': self.branch_ids.ids,
            'journals': self.journal_ids.ids,
            'accounts': self.account_ids.ids,
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
        return self.env.ref('branch_accounting_report.action_branch_accounting_report').report_action(self, data=data)