from odoo import models, fields, api, _
from datetime import datetime

class FinancialReport(models.Model):
    _name = 'taknia.financial.report'
    _description = 'Advanced Financial Report'
    
    name = fields.Char(string='Report Name', required=True, default='Financial Report')
    report_date = fields.Date(string='Report Date', default=fields.Date.context_today)
    branch_id = fields.Many2one('res.branch', string='Branch')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)
    
    total_assets = fields.Monetary(string='Total Assets', currency_field='currency_id')
    total_liabilities = fields.Monetary(string='Total Liabilities', currency_field='currency_id')
    total_equity = fields.Monetary(string='Total Equity', currency_field='currency_id')
    net_profit = fields.Monetary(string='Net Profit', currency_field='currency_id')
    revenue = fields.Monetary(string='Total Revenue', currency_field='currency_id')
    expenses = fields.Monetary(string='Total Expenses', currency_field='currency_id')

    @api.model
    def calculate_financials(self, date_from, date_to, branch_id=None):
        """Core calculation logic for financial data"""
        domain = [('date', '>=', date_from), ('date', '<=', date_to)]
        if branch_id:
            domain.append(('branch_id', '=', branch_id))

        account_moves = self.env['account.move.line'].search(domain)

        revenue = sum(account_moves.filtered(lambda l: l.account_id.user_type_id.type == 'income').mapped('balance'))
        expenses = sum(account_moves.filtered(lambda l: l.account_id.user_type_id.type == 'expense').mapped('balance'))
        assets = sum(account_moves.filtered(lambda l: l.account_id.user_type_id.type == 'asset').mapped('balance'))
        liabilities = sum(account_moves.filtered(lambda l: l.account_id.user_type_id.type == 'liability').mapped('balance'))

        equity = assets - liabilities
        net_profit = revenue - expenses

        return {
            'total_assets': assets,
            'total_liabilities': liabilities,
            'total_equity': equity,
            'net_profit': net_profit,
            'revenue': revenue,
            'expenses': expenses,
        }

    def action_generate_report(self):
        """Button to calculate and update report fields"""
        financial_data = self.calculate_financials(datetime.today().replace(day=1), fields.Date.today(), self.branch_id.id)

        self.write(financial_data)

    def action_export_pdf(self):
        """Export the report to PDF"""
        return self.env.ref('taknia_advanced_accounting.financial_report_pdf').report_action(self)

    def action_export_excel(self):
        """Export the report to Excel"""
        return self.env.ref('taknia_advanced_accounting.financial_report_excel').report_action(self)

    def action_send_advice(self):
        """Trigger AI financial advice based on the report"""
        advice = self.env['taknia.financial.advice.ai'].get_advice(self)
        message = _("AI Financial Advice: %s") % advice
        self.message_post(body=message)
