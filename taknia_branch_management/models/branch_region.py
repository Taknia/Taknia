from odoo import models, fields, api, _

class BranchRegion(models.Model):
    _name = 'taknia.branch.region'
    _description = 'Branch Region'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(required=True, tracking=True)
    code = fields.Char(required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                default=lambda self: self.env.company)
    manager_id = fields.Many2one('hr.employee', string='Regional Manager', tracking=True)
    
    # Branches
    branch_ids = fields.One2many('taknia.branch', 'region_id', string='Branches')
    branch_count = fields.Integer(compute='_compute_branch_count')
    active_branch_count = fields.Integer(compute='_compute_branch_count')
    
    # Regional Statistics
    total_employees = fields.Integer(compute='_compute_regional_stats')
    total_customers = fields.Integer(compute='_compute_regional_stats')
    total_revenue = fields.Monetary(compute='_compute_regional_stats', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    
    # Performance
    performance_score = fields.Float(compute='_compute_performance')
    growth_rate = fields.Float(compute='_compute_growth_rate')
    
    @api.depends('branch_ids')
    def _compute_branch_count(self):
        for record in self:
            record.branch_count = len(record.branch_ids)
            record.active_branch_count = len(record.branch_ids.filtered('active'))
    
    @api.depends('branch_ids', 'branch_ids.employee_count', 
                'branch_ids.customer_count', 'branch_ids.actual_revenue')
    def _compute_regional_stats(self):
        for record in self:
            record.total_employees = sum(record.branch_ids.mapped('employee_count'))
            record.total_customers = sum(record.branch_ids.mapped('customer_count'))
            record.total_revenue = sum(record.branch_ids.mapped('actual_revenue'))
    
    @api.depends('branch_ids.performance_score')
    def _compute_performance(self):
        for record in self:
            if record.branch_ids:
                scores = record.branch_ids.mapped('performance_score')
                record.performance_score = sum(scores) / len(scores)
            else:
                record.performance_score = 0.0
    
    @api.depends('branch_ids.actual_revenue')
    def _compute_growth_rate(self):
        for record in self:
            # To be implemented: Calculate YoY growth rate
            record.growth_rate = 0.0
    
    @api.constrains('code')
    def _check_unique_code(self):
        for record in self:
            existing = self.search([
                ('code', '=', record.code),
                ('id', '!=', record.id),
                ('company_id', '=', record.company_id.id)
            ])
            if existing:
                raise ValidationError(_('Region code must be unique within the same company!'))
