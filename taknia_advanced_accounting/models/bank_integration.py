from odoo import models, fields, api, _
from datetime import datetime

class BankIntegration(models.Model):
    _name = 'taknia.bank.integration'
    _description = 'Bank Integration - Financial Flow Analysis'

    name = fields.Char(string="Bank Name", required=True)
    connection_status = fields.Selection([
        ('connected', 'Connected'),
        ('disconnected', 'Disconnected'),
        ('error', 'Connection Error')
    ], string="Connection Status", default='disconnected')

    last_sync_date = fields.Datetime(string="Last Sync Date")
    total_inflows = fields.Float(string="Total Inflows", readonly=True)
    total_outflows = fields.Float(string="Total Outflows", readonly=True)
    net_cash_flow = fields.Float(string="Net Cash Flow", readonly=True)
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)

    transaction_count = fields.Integer(string="Number of Transactions", readonly=True)

    @api.model
    def sync_bank_transactions(self):
        """محاكاة عملية جلب وتحليل التدفقات البنكية من بنك متكامل مع أودو"""
        banks = self.search([])
        for bank in banks:
            try:
                # هنا يتم استدعاء API فعلي (في التطبيق الفعلي)، الآن مجرد محاكاة.
                inflows, outflows, transactions = self._mock_bank_transactions()

                bank.write({
                    'connection_status': 'connected',
                    'last_sync_date': datetime.now(),
                    'total_inflows': inflows,
                    'total_outflows': outflows,
                    'net_cash_flow': inflows - outflows,
                    'transaction_count': transactions,
                })
            except Exception as e:
                bank.write({
                    'connection_status': 'error',
                })
                _logger.error(f"Bank Sync Failed for {bank.name}: {e}")

    def _mock_bank_transactions(self):
        """هذه دالة محاكاة - يتم استبدالها لاحقًا بربط فعلي مع البنك"""
        import random
        inflows = random.uniform(50000, 200000)
        outflows = random.uniform(30000, 150000)
        transactions = random.randint(50, 500)
        return inflows, outflows, transactions

    def action_view_transactions(self):
        """زر لعرض الحركات التفصيلية لو أردت لاحقًا"""
        # مخصص لو ربطنا بجدول معاملات فعلي لاحقًا
        return {
            'type': 'ir.actions.act_window',
            'name': _('Bank Transactions'),
            'res_model': 'account.bank.statement.line',
            'view_mode': 'tree,form',
            'domain': [('date', '>=', datetime.now().replace(day=1))],
            'context': {'default_company_id': self.company_id.id},
        }
