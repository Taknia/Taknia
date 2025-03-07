from odoo import models, fields, api
from collections import defaultdict

class BranchStockAnalysis(models.Model):
    _name = 'branch.stock.analysis'
    _description = 'Branch Stock Analysis'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Analysis Name', required=True, default='New Stock Analysis', tracking=True)
    branch_id = fields.Many2one('res.branch', string='Branch', required=True, tracking=True)
    analysis_date = fields.Date(string='Analysis Date', default=fields.Date.today, tracking=True)

    total_stock_value = fields.Float(string='Total Stock Value', compute='_compute_stock_metrics', store=True, tracking=True)
    top_products = fields.Text(string='Top Products by Value', compute='_compute_stock_metrics', store=True, tracking=True)
    low_stock_products = fields.Text(string='Low Stock Products', compute='_compute_stock_metrics', tracking=True)

    @api.depends('branch_id')
    def _compute_stock_metrics(self):
        for record in self:
            if not record.branch_id:
                record.total_stock_value = 0.0
                record.top_products = ''
                record.low_stock_products = ''
                continue

            location_ids = self.env['stock.location'].search([('branch_id', '=', record.branch_id.id), ('usage', '=', 'internal')])

            product_data = defaultdict(lambda: {'qty': 0, 'value': 0})
            quant_obj = self.env['stock.quant']

            for location in location_ids:
                quants = quant_obj.search([('location_id', '=', location.id)])
                for quant in quants:
                    product_data[quant.product_id]['qty'] += quant.quantity
                    product_data[quant.product_id]['value'] += quant.quantity * quant.product_id.standard_price

            total_stock_value = sum(data['value'] for data in product_data.values())
            record.total_stock_value = total_stock_value

            # Top 5 Products by Value
            sorted_products = sorted(product_data.items(), key=lambda item: item[1]['value'], reverse=True)
            top_products = "\n".join([f"{product.display_name}: {data['value']:.2f}" for product, data in sorted_products[:5]])
            record.top_products = top_products

            # Low Stock Products (أقل من 5 وحدات)
            low_stock_products = [f"{product.display_name}: {data['qty']} units" for product, data in product_data.items() if data['qty'] < 5]
            record.low_stock_products = "\n".join(low_stock_products)

    def action_refresh_analysis(self):
        self._compute_stock_metrics()
