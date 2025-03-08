from odoo import models, fields

class BranchExpenseAnalysis(models.Model):
    _name = 'branch.expense.analysis'
    _description = 'Branch Expense Analysis'

    branch_id = fields.Many2one('branch', 'Branch', required=True)
    expense_category = fields.Char('Expense Category', required=True)
    amount = fields.Float('Amount')
    date = fields.Date('Date', required=True)