from odoo import models, fields

class BranchStockAnalysis(models.Model):
    _name = 'branch.stock.analysis'
    _description = 'Branch Stock Analysis'

    branch_id = fields.Many2one('branch', 'Branch', required=True)
    product_id = fields.Many2one('product.product', 'Product', required=True)
    stock_level = fields.Float('Stock Level')
    date = fields.Date('Date', required=True)