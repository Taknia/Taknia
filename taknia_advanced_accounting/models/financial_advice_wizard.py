from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class FinancialAdviceWizard(models.TransientModel):
    _name = 'financial.advice.wizard'
    _description = 'Financial Advice Wizard'

    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    branch_id = fields.Many2one('res.branch', string='Branch', required=False)
    advice_type = fields.Selection([
        ('cashflow', 'Cash Flow Analysis'),
        ('profitability', 'Profitability Analysis'),
        ('debt', 'Debt Management Advice'),
        ('custom', 'Custom Advice')
    ], string='Advice Type', required=True)

    def action_get_advice(self):
        advice = self._fetch_financial_advice()
        self._show_advice_popup(advice)

    def _fetch_financial_advice(self):
        # هنا ندمج مع ChatGPT أو الذكاء الاصطناعي لتوليد النصيحة بناءً على البيانات
        financial_data = self._gather_financial_data()
        advice_text = self._get_ai_advice(financial_data)
        return advice_text

    def _gather_financial_data(self):
        domain = [('date', '>=', self.date_from), ('date', '<=', self.date_to)]
        if self.branch_id:
            domain.append(('branch_id', '=', self.branch_id.id))

        moves = self.env['account.move.line'].search(domain)
        data = {
            'total_debit': sum(moves.mapped('debit')),
            'total_credit': sum(moves.mapped('credit')),
            'balance': sum(moves.mapped(lambda m: m.debit - m.credit)),
        }
        return data

    def _get_ai_advice(self, data):
        # محاكاة استدعاء ChatGPT API
        advice_template = f"""
        Financial Health Analysis:
        Total Debit: {data['total_debit']:.2f}
        Total Credit: {data['total_credit']:.2f}
        Net Balance: {data['balance']:.2f}

        Based on the selected advice type ({self.advice_type}), we recommend the following:
        """

        if self.advice_type == 'cashflow':
            advice_template += "Focus on maintaining positive cash flows, optimize receivables collection, and control excessive spending."
        elif self.advice_type == 'profitability':
            advice_template += "Analyze product-level profitability, review pricing strategies, and reduce operational inefficiencies."
        elif self.advice_type == 'debt':
            advice_template += "Ensure debt-to-equity ratio is within safe limits, and consider refinancing high-interest debts."
        else:
            advice_template += "This is a customized financial advice based on your business data."

        return advice_template

    def _show_advice_popup(self, advice):
        return {
            'name': 'Financial Advice',
            'type': 'ir.actions.act_window',
            'res_model': 'financial.advice.result',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_advice_text': advice},
        }
