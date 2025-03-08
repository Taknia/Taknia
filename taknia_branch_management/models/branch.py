from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Branch(models.Model):
    _name = 'taknia.branch'
    _description = 'Branch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, name'

    name = fields.Char(string='Branch Name', required=True, tracking=True)
    code = fields.Char(string='Branch Code', required=True, tracking=True)
    sequence = fields.Integer(string='Sequence', default=10)
    company_id = fields.Many2one('res.company', string='Company', required=True, 
                                default=lambda self: self.env.company)
    active = fields.Boolean(default=True, tracking=True)

    # Location and Contact
    street = fields.Char(tracking=True)
    street2 = fields.Char(tracking=True)
    city = fields.Char(tracking=True)
    state_id = fields.Many2one('res.country.state', tracking=True)
    zip = fields.Char(tracking=True)
    country_id = fields.Many2one('res.country', tracking=True)
    phone = fields.Char(tracking=True)
    email = fields.Char(tracking=True)
    website = fields.Char(tracking=True)

    # Management
    manager_id = fields.Many2one('hr.employee', string='Branch Manager', tracking=True)
    region_id = fields.Many2one('taknia.branch.region', string='Region', tracking=True)
    opening_date = fields.Date(string='Opening Date', tracking=True)
    establishment_year = fields.Integer(compute='_compute_establishment_year', store=True)

    # Operations
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    operating_hours = fields.Text(string='Operating Hours')
    is_main_branch = fields.Boolean(string='Main Branch', default=False)
    branch_type = fields.Selection([
        ('retail', 'Retail'),
        ('wholesale', 'Wholesale'),
        ('service', 'Service Center'),
        ('warehouse', 'Warehouse'),
    ], string='Branch Type', required=True, default='retail')

    # Financial
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    budget = fields.Monetary(string='Annual Budget', currency_field='currency_id', tracking=True)
    revenue_target = fields.Monetary(string='Revenue Target', currency_field='currency_id')
    actual_revenue = fields.Monetary(string='Actual Revenue', compute='_compute_actual_revenue')
    profit_margin = fields.Float(string='Profit Margin %', compute='_compute_profit_margin')

    # ESG Metrics
    energy_consumption = fields.Float(string='Energy Consumption (kWh)')
    water_usage = fields.Float(string='Water Usage (m³)')
    waste_recycled = fields.Float(string='Waste Recycled (%)')
    community_programs = fields.Integer(string='Community Programs')

    # Statistics
    employee_count = fields.Integer(compute='_compute_employee_count', string='Employees')
    customer_count = fields.Integer(compute='_compute_customer_count', string='Customers')
    satisfaction_score = fields.Float(string='Customer Satisfaction', compute='_compute_satisfaction')
    performance_score = fields.Float(string='Performance Score', compute='_compute_performance')

    @api.constrains('code')
    def _check_unique_code(self):
        for record in self:
            existing = self.search([
                ('code', '=', record.code),
                ('id', '!=', record.id),
                ('company_id', '=', record.company_id.id)
            ])
            if existing:
                raise ValidationError(_('Branch code must be unique within the same company!'))

    @api.depends('opening_date')
    def _compute_establishment_year(self):
        for record in self:
            if record.opening_date:
                record.establishment_year = record.opening_date.year
            else:
                record.establishment_year = False

    @api.depends('name')
    def _compute_employee_count(self):
        for record in self:
            record.employee_count = self.env['hr.employee'].search_count([
                ('branch_id', '=', record.id)
            ])

    @api.depends('name')
    def _compute_customer_count(self):
        for record in self:
            record.customer_count = self.env['res.partner'].search_count([
                ('branch_id', '=', record.id)
            ])

    @api.depends('name')
    def _compute_actual_revenue(self):
        for record in self:
            # To be implemented: Calculate actual revenue from account moves
            record.actual_revenue = 0.0

    @api.depends('actual_revenue', 'revenue_target')
    def _compute_profit_margin(self):
        for record in self:
            if record.revenue_target and record.revenue_target != 0:
                record.profit_margin = (record.actual_revenue / record.revenue_target) * 100
            else:
                record.profit_margin = 0.0

    @api.depends('name')
    def _compute_satisfaction(self):
        for record in self:
            # To be implemented: Calculate satisfaction from feedback
            record.satisfaction_score = 0.0

    @api.depends('employee_count', 'customer_count', 'profit_margin', 'satisfaction_score')
    def _compute_performance(self):
        for record in self:
            # Weighted average of various metrics
            record.performance_score = (
                record.profit_margin * 0.4 +
                record.satisfaction_score * 0.3 +
                min(record.employee_count / 100, 1) * 0.15 +
                min(record.customer_count / 1000, 1) * 0.15
            )

class BranchRegion(models.Model):
    _name = 'taknia.branch.region'
    _description = 'Branch Region'
    
    name = fields.Char(required=True)
    code = fields.Char(required=True)
    manager_id = fields.Many2one('hr.employee', string='Regional Manager')
    branch_ids = fields.One2many('taknia.branch', 'region_id', string='Branches')
    branch_count = fields.Integer(compute='_compute_branch_count')
    
    @api.depends('branch_ids')
    def _compute_branch_count(self):
        for record in self:
            record.branch_count = len(record.branch_ids)