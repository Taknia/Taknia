from odoo import models, fields, api

class ProductBranchAnalysis(models.Model):
    _name = 'taknia.product.analysis'
    _description = 'Product Analysis Per Branch'

    branch_id = fields.Many2one('taknia.branch', string='Branch', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    total_sales = fields.Float(string='Total Sales', compute='_compute_total_sales', store=True)
    total_quantity_sold = fields.Float(string='Total Quantity Sold', compute='_compute_total_quantity', store=True)
    revenue_generated = fields.Float(string='Revenue Generated', compute='_compute_revenue_generated', store=True)

    @api.depends('product_id', 'branch_id')
    def _compute_total_sales(self):
        for record in self:
            record.total_sales = sum(self.env['sale.order.line'].search([('product_id', '=', record.product_id.id), ('order_id.branch_id', '=', record.branch_id.id)]).mapped('price_subtotal'))

    @api.depends('product_id', 'branch_id')
    def _compute_total_quantity(self):
        for record in self:
            record.total_quantity_sold = sum(self.env['sale.order.line'].search([('product_id', '=', record.product_id.id), ('order_id.branch_id', '=', record.branch_id.id)]).mapped('product_uom_qty'))

    @api.depends('total_sales')
    def _compute_revenue_generated(self):
        for record in self:
            record.revenue_generated = record.total_sales