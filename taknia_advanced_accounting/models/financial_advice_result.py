from odoo import models, fields

class FinancialAdviceResult(models.TransientModel):
    _name = 'financial.advice.result'
    _description = 'Financial Advice Result'

    advice_text = fields.Text(string='Advice', readonly=True)
