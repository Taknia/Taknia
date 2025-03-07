from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class RegionalManagement(models.Model):
    _name = 'regional.management'
    _description = 'Regional Management'
    _rec_name = 'name'

    name = fields.Char(string='Region Name', required=True, unique=True)
    manager_id = fields.Many2one('res.users', string='Regional Manager', required=True)
    branch_ids = fields.One2many('res.branch', 'region_id', string='Branches')
    total_branches = fields.Integer(string='Total Branches', compute='_compute_total_branches', store=True)
    
    total_revenue = fields.Float(string='Total Revenue', compute='_compute_total_financials', store=True)
    total_expenses = fields.Float(string='Total Expenses', compute='_compute_total_financials', store=True)
    net_profit = fields.Float(string='Net Profit', compute='_compute_total_financials', store=True)
    
    region_performance_score = fields.Float(string='Performance Score', compute='_compute_performance_score', store=True)
    region_status = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor')
    ], string='Region Status', compute='_compute_region_status', store=True)

    notes = fields.Text(string='Notes')

    # ----------------------------------------
    # حساب إجمالي عدد الفروع
    # ----------------------------------------
    @api.depends('branch_ids')
    def _compute_total_branches(self):
        for record in self:
            record.total_branches = len(record.branch_ids)

    # ----------------------------------------
    # حساب البيانات المالية للأقليم
    # ----------------------------------------
    @api.depends('branch_ids')
    def _compute_total_financials(self):
        for record in self:
            total_revenue = sum(record.branch_ids.mapped('total_revenue'))
            total_expenses = sum(record.branch_ids.mapped('total_expenses'))
            record.total_revenue = total_revenue
            record.total_expenses = total_expenses
            record.net_profit = total_revenue - total_expenses

    # ----------------------------------------
    # حساب درجة أداء الأقليم بناءً على الفروع
    # ----------------------------------------
    @api.depends('branch_ids')
    def _compute_performance_score(self):
        for record in self:
            if record.branch_ids:
                total_score = sum(record.branch_ids.mapped('branch_performance_score'))
                record.region_performance_score = total_score / len(record.branch_ids)
            else:
                record.region_performance_score = 50.0  # افتراضي

    # ----------------------------------------
    # تصنيف حالة الأقليم بناءً على الأداء
    # ----------------------------------------
    @api.depends('region_performance_score')
    def _compute_region_status(self):
        for record in self:
            if record.region_performance_score >= 85:
                record.region_status = 'excellent'
            elif record.region_performance_score >= 70:
                record.region_status = 'good'
            elif record.region_performance_score >= 50:
                record.region_status = 'average'
            else:
                record.region_status = 'poor'

    # ----------------------------------------
    # التأكد من أن الإقليم لا يتكرر
    # ----------------------------------------
    @api.constrains('name')
    def _check_unique_region(self):
        for record in self:
            existing_region = self.search([('name', '=', record.name), ('id', '!=', record.id)])
            if existing_region:
                raise ValidationError(_('Region name must be unique!'))

    # ----------------------------------------
    # فتح تفاصيل الفروع داخل الأقليم
    # ----------------------------------------
    def action_open_branches(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Branches in Region'),
            'res_model': 'res.branch',
            'view_mode': 'tree,form',
            'domain': [('region_id', '=', self.id)],
            'context': {'default_region_id': self.id},
        }
