from odoo import models, fields, api
from datetime import date, timedelta

class BranchCustomerAnalysis(models.Model):
    _name = 'branch.customer.analysis'
    _description = 'Branch Customer Profitability Analysis'

    name = fields.Char(string='Analysis Name', required=True, default='New Customer Analysis')
    branch_id = fields.Many2one('res.branch', string='Branch', required=True)
    analysis_date = fields.Date(string='Analysis Date', default=fields.Date.today)

    total_customers = fields.Integer(string='Total Customers', compute='_compute_customer_metrics')
    active_customers = fields.Integer(string='Active Customers', compute='_compute_customer_metrics')
    inactive_customers = fields.Integer(string='Inactive Customers', compute='_compute_customer_metrics')
    top_profitable_customers = fields.Text(string='Top Profitable Customers', compute='_compute_customer_metrics')
    low_profitable_customers = fields.Text(string='Low Profitable Customers', compute='_compute_customer_metrics')

    @api.depends('branch_id')
    def _compute_customer_metrics(self):
        for record in self:
            if not record.branch_id:
                record.total_customers = 0
                record.active_customers = 0
                record.inactive_customers = 0
                record.top_profitable_customers = ""
                record.low_profitable_customers = ""
                continue

            partners = self.env['res.partner'].search([('branch_id', '=', record.branch_id.id)])
            record.total_customers = len(partners)

            active_customers = partners.filtered(lambda p: p.sale_order_count > 0)
            record.active_customers = len(active_customers)
            record.inactive_customers = len(partners) - len(active_customers)

            profitability_data = []
            for partner in active_customers:
                total_sales = sum(partner.sale_order_ids.mapped('amount_total'))
                profitability_data.append((partner.name, total_sales))

            profitability_data.sort(key=lambda x: x[1], reverse=True)
            record.top_profitable_customers = "\n".join([f"{name}: {amount:.2f}" for name, amount in profitability_data[:5]])
            record.low_profitable_customers = "\n".join([f"{name}: {amount:.2f}" for name, amount in profitability_data[-5:]])

    def action_refresh_analysis(self):
        self._compute_customer_metrics()
