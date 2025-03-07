from odoo import models, fields, api
from datetime import date, timedelta

class BranchExpenseAnalysis(models.Model):
    _name = 'branch.expense.analysis'
    _description = 'Branch Expense Analysis'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Analysis Name', required=True, default='New Expense Analysis', tracking=True)
    branch_id = fields.Many2one('res.branch', string='Branch', required=True, tracking=True)
    analysis_date = fields.Date(string='Analysis Date', default=fields.Date.today, tracking=True)

    total_expenses = fields.Float(string='Total Expenses', compute='_compute_expense_metrics', store=True, tracking=True)
    top_expense_categories = fields.Text(string='Top Expense Categories', compute='_compute_expense_metrics', store=True, tracking=True)
    expense_trend = fields.Text(string='Monthly Expense Trend', compute='_compute_expense_metrics', tracking=True)

    @api.depends('branch_id')
    def _compute_expense_metrics(self):
        for record in self:
            if not record.branch_id:
                record.total_expenses = 0.0
                record.top_expense_categories = ''
                record.expense_trend = ''
                continue

            # جمع المصروفات حسب حسابات محددة مرتبطة بالفرع
            account_moves = self.env['account.move.line'].search([
                ('branch_id', '=', record.branch_id.id),
                ('move_id.move_type', '=', 'entry'),
                ('account_id.internal_group', '=', 'expense'),
            ])

            total_expenses = sum(account_moves.mapped('balance'))
            record.total_expenses = abs(total_expenses)

            # تحليل أكثر الفئات صرفًا
            category_expense = {}
            for line in account_moves:
                account_name = line.account_id.name
                category_expense[account_name] = category_expense.get(account_name, 0) + abs(line.balance)

            sorted_expenses = sorted(category_expense.items(), key=lambda x: x[1], reverse=True)
            top_categories = "\n".join([f"{cat}: {amount:.2f}" for cat, amount in sorted_expenses[:5]])
            record.top_expense_categories = top_categories

            # تحليل اتجاه المصروفات الشهري
            monthly_expenses = {}
            for line in account_moves:
                month = line.date.strftime('%Y-%m')
                monthly_expenses[month] = monthly_expenses.get(month, 0) + abs(line.balance)

            trend_lines = [f"{month}: {amount:.2f}" for month, amount in sorted(monthly_expenses.items())]
            record.expense_trend = "\n".join(trend_lines)

    def action_refresh_analysis(self):
        self._compute_expense_metrics()
