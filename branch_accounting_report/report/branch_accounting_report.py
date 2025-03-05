from odoo import models, api

class BranchAccountingReport(models.AbstractModel):
    _name = 'report.branch_accounting_report.branch_accounting_report_template'
    _description = 'Branch Accounting Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        branch_option = data.get('branch_option')
        branches = self.env['res.branch'].browse(data.get('branches')) if branch_option == 'specific' else self.env['res.branch'].search([])
        journals = self.env['account.journal'].browse(data.get('journals'))
        accounts = self.env['account.account'].browse(data.get('accounts'))
        date_from = data.get('date_from')
        date_to = data.get('date_to')

        moves = self.env['account.move'].search([
            ('branch_id', 'in', branches.ids),
            ('journal_id', 'in', journals.ids),
            ('line_ids.account_id', 'in', accounts.ids),
            ('date', '>=', date_from),
            ('date', '<=', date_to),
            ('state', '=', 'posted')
        ])

        return {
            'docs': moves,
            'branches': branches,
            'date_from': date_from,
            'date_to': date_to,
            'journals': journals,
            'accounts': accounts,
        }