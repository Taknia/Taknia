from odoo import models, fields, api, _
from datetime import date, timedelta

class FinancialKPIDashboard(models.Model):
    _name = 'taknia.financial.kpi.dashboard'
    _description = 'Financial KPI Dashboard'

    name = fields.Char(string="Dashboard Name", default="Financial KPI Dashboard")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)

    revenue_current_month = fields.Float(string="Revenue - Current Month")
    revenue_last_month = fields.Float(string="Revenue - Last Month")
    profit_margin = fields.Float(string="Profit Margin (%)")
    liquidity_ratio = fields.Float(string="Liquidity Ratio")
    debt_ratio = fields.Float(string="Debt Ratio")
    accounts_receivable_days = fields.Float(string="AR Collection Period (Days)")
    accounts_payable_days = fields.Float(string="AP Payment Period (Days)")
    inventory_turnover = fields.Float(string="Inventory Turnover")
    customer_profitability = fields.Float(string="Top Customer Profitability (%)")
    financial_health_score = fields.Float(string="Financial Health Score")

    @api.model
    def update_dashboard(self):
        """تحديث بيانات لوحة المؤشرات بناءً على بيانات حية من الحسابات"""
        dashboard = self.search([], limit=1) or self.create({})

        today = date.today()
        first_day_current_month = today.replace(day=1)
        first_day_last_month = (first_day_current_month - timedelta(days=1)).replace(day=1)
        last_day_last_month = first_day_current_month - timedelta(days=1)

        # الإيرادات الحالية
        revenue_current = self._get_total_revenue(first_day_current_month, today)
        revenue_last = self._get_total_revenue(first_day_last_month, last_day_last_month)

        # هامش الربح
        profit_margin = self._calculate_profit_margin()

        # نسب السيولة والدين
        liquidity_ratio = self._calculate_liquidity_ratio()
        debt_ratio = self._calculate_debt_ratio()

        # تحليل الذمم المدينة والدائنة
        ar_days = self._calculate_ar_collection_period()
        ap_days = self._calculate_ap_payment_period()

        # دوران المخزون
        inventory_turnover = self._calculate_inventory_turnover()

        # أفضل عميل
        top_customer_profitability = self._calculate_top_customer_profitability()

        # التقييم الصحي للشركة
        financial_health_score = self._calculate_financial_health_score(liquidity_ratio, debt_ratio, profit_margin)

        dashboard.write({
            'revenue_current_month': revenue_current,
            'revenue_last_month': revenue_last,
            'profit_margin': profit_margin,
            'liquidity_ratio': liquidity_ratio,
            'debt_ratio': debt_ratio,
            'accounts_receivable_days': ar_days,
            'accounts_payable_days': ap_days,
            'inventory_turnover': inventory_turnover,
            'customer_profitability': top_customer_profitability,
            'financial_health_score': financial_health_score,
        })

    def _get_total_revenue(self, start_date, end_date):
        """إجمالي الإيرادات"""
        invoices = self.env['account.move'].search([
            ('invoice_date', '>=', start_date),
            ('invoice_date', '<=', end_date),
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
        ])
        return sum(invoices.mapped('amount_total'))

    def _calculate_profit_margin(self):
        """حساب هامش الربح"""
        profit = self._get_net_profit()
        revenue = self._get_total_revenue(date.today().replace(day=1), date.today())
        return (profit / revenue * 100) if revenue else 0.0

    def _get_net_profit(self):
        """حساب صافي الربح (الإيرادات - المصروفات)"""
        revenues = self._get_total_revenue(date.today().replace(day=1), date.today())
        expenses = self._get_total_expenses(date.today().replace(day=1), date.today())
        return revenues - expenses

    def _get_total_expenses(self, start_date, end_date):
        """إجمالي المصروفات"""
        expenses = self.env['account.move'].search([
            ('invoice_date', '>=', start_date),
            ('invoice_date', '<=', end_date),
            ('move_type', '=', 'in_invoice'),
            ('state', '=', 'posted'),
        ])
        return sum(expenses.mapped('amount_total'))

    def _calculate_liquidity_ratio(self):
        """نسبة السيولة (الأصول المتداولة ÷ الالتزامات المتداولة)"""
        balance_sheet = self.env['account.balance.report'].generate_balance_sheet()
        current_assets = balance_sheet.get('current_assets', 1)
        current_liabilities = balance_sheet.get('current_liabilities', 1)
        return current_assets / current_liabilities

    def _calculate_debt_ratio(self):
        """نسبة الدين (إجمالي الالتزامات ÷ إجمالي الأصول)"""
        balance_sheet = self.env['account.balance.report'].generate_balance_sheet()
        total_liabilities = balance_sheet.get('total_liabilities', 1)
        total_assets = balance_sheet.get('total_assets', 1)
        return total_liabilities / total_assets

    def _calculate_ar_collection_period(self):
        """متوسط فترة تحصيل الذمم المدينة"""
        ar_balance = self.env['account.move.line'].search([
            ('account_id.internal_type', '=', 'receivable'),
            ('move_id.state', '=', 'posted'),
        ])
        total_ar = sum(ar_balance.mapped('balance'))
        monthly_sales = self._get_total_revenue(date.today().replace(day=1), date.today())
        return (total_ar / monthly_sales * 30) if monthly_sales else 0.0

    def _calculate_ap_payment_period(self):
        """متوسط فترة سداد الذمم الدائنة"""
        ap_balance = self.env['account.move.line'].search([
            ('account_id.internal_type', '=', 'payable'),
            ('move_id.state', '=', 'posted'),
        ])
        total_ap = sum(ap_balance.mapped('balance'))
        monthly_purchases = self._get_total_expenses(date.today().replace(day=1), date.today())
        return (total_ap / monthly_purchases * 30) if monthly_purchases else 0.0

    def _calculate_inventory_turnover(self):
        """دوران المخزون"""
        stock_moves = self.env['stock.move'].search([
            ('state', '=', 'done'),
            ('date', '>=', date.today().replace(day=1)),
            ('date', '<=', date.today()),
        ])
        total_cogs = sum(stock_moves.filtered(lambda m: m.location_id.usage == 'internal').mapped('value'))
        average_inventory = self._get_average_inventory()
        return (total_cogs / average_inventory) if average_inventory else 0.0

    def _get_average_inventory(self):
        """متوسط المخزون"""
        inventory_vals = self.env['stock.quant'].search([])
        return sum(inventory_vals.mapped('inventory_value')) / 2

    def _calculate_top_customer_profitability(self):
        """تحليل أعلى ربحية للعملاء"""
        customer_profits = {}
        invoices = self.env['account.move'].search([
            ('move_type', '=', 'out_invoice'),
            ('state', '=', 'posted'),
        ])
        for invoice in invoices:
            profit = invoice.amount_total - sum(invoice.invoice_line_ids.mapped('purchase_price'))
            customer_profits[invoice.partner_id.id] = customer_profits.get(invoice.partner_id.id, 0) + profit

        if customer_profits:
            top_customer_profit = max(customer_profits.values())
            total_profit = sum(customer_profits.values())
            return (top_customer_profit / total_profit * 100) if total_profit else 0.0
        return 0.0

    def _calculate_financial_health_score(self, liquidity, debt, profit_margin):
        """تقييم الصحة المالية بناءً على مؤشرات"""
        score = (liquidity * 30) + ((1 - debt) * 30) + (profit_margin * 40)
        return min(max(score, 0), 100)  # بين 0 و 100
