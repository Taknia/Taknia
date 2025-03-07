from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)

class ProductCostAnalysis(models.Model):
    _name = 'product.cost.analysis'
    _description = 'Product Cost Analysis'
    
    product_id = fields.Many2one('product.product', string="Product", required=True)
    total_cost = fields.Float(string="Total Cost", compute='_compute_total_cost', store=True)
    direct_cost = fields.Float(string="Direct Cost (COGS)")
    indirect_cost = fields.Float(string="Indirect Cost")
    profitability_ratio = fields.Float(string="Profitability Ratio (%)", compute='_compute_profitability', store=True)
    last_analysis_date = fields.Datetime(string="Last Analysis Date")

    @api.depends('direct_cost', 'indirect_cost')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.direct_cost + record.indirect_cost

    @api.depends('product_id', 'total_cost')
    def _compute_profitability(self):
        for record in self:
            sales_price = record.product_id.lst_price
            if record.total_cost > 0:
                record.profitability_ratio = ((sales_price - record.total_cost) / sales_price) * 100
            else:
                record.profitability_ratio = 0

    def action_analyze_product_cost(self):
        for record in self:
            record._calculate_product_cost()

    def _calculate_product_cost(self):
        self.ensure_one()

        # حساب التكلفة المباشرة (Direct Cost) من تحركات المخزون أو BOM
        bom_cost = self._get_bom_cost()
        stock_moves_cost = self._get_stock_moves_cost()

        self.direct_cost = bom_cost if bom_cost > 0 else stock_moves_cost

        # حساب التكلفة غير المباشرة (Indirect Cost) (تقديرية - يمكن تحسينها حسب التكاليف الفعلية)
        self.indirect_cost = self._estimate_indirect_cost()

        # تحديث باقي الحقول
        self.last_analysis_date = fields.Datetime.now()

        # إعادة حساب التكاليف والربحية
        self._compute_total_cost()
        self._compute_profitability()

        _logger.info(f"Product Cost Analysis updated for {self.product_id.name}")

    def _get_bom_cost(self):
        """ استرجاع تكلفة المنتج من الBOM لو موجود """
        bom = self.env['mrp.bom'].search([('product_tmpl_id', '=', self.product_id.product_tmpl_id.id)], limit=1)
        if bom:
            return bom.total_cost or 0.0
        return 0.0

    def _get_stock_moves_cost(self):
        """ حساب متوسط تكلفة المنتج من تحركات المخزون """
        moves = self.env['stock.move'].search([
            ('product_id', '=', self.product_id.id),
            ('state', '=', 'done'),
            ('price_unit', '>', 0)
        ])
        total_cost = sum(moves.mapped('value'))
        total_qty = sum(moves.mapped('product_qty'))
        if total_qty > 0:
            return total_cost / total_qty
        return 0.0

    def _estimate_indirect_cost(self):
        """ تقدير التكاليف غير المباشرة (مصروفات إدارية - كهرباء - إلخ) كنسبة مئوية ثابتة مؤقتة """
        return self.direct_cost * 0.15  # 15% نسبة تقديرية كنموذج مبدأي

    @api.model
    def cron_automatic_product_cost_analysis(self):
        """ كرون جوب لتحليل التكاليف بشكل دوري لجميع المنتجات """
        products = self.search([])
        for record in products:
            try:
                record._calculate_product_cost()
            except Exception as e:
                _logger.error(f"Failed to analyze product cost for {record.product_id.name}: {str(e)}")
