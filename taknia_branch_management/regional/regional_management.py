from odoo import models, fields, api

class RegionalManagement(models.Model):
    _name = 'taknia.regional.management'
    _description = 'Regional Branch Management'

    region_name = fields.Char(string='Region Name', required=True)
    branch_ids = fields.One2many('taknia.branch', 'region_id', string='Branches')
    total_revenue = fields.Float(string='Total Revenue', compute='_compute_total_revenue', store=True)
    total_expenses = fields.Float(string='Total Expenses', compute='_compute_total_expenses', store=True)
    performance_score = fields.Float(string='Performance Score', compute='_compute_performance_score', store=True)

    @api.depends('branch_ids.revenue')
    def _compute_total_revenue(self):
        for record in self:
            record.total_revenue = sum(record.branch_ids.mapped('revenue'))

    @api.depends('branch_ids.expenses')
    def _compute_total_expenses(self):
        for record in self:
            record.total_expenses = sum(record.branch_ids.mapped('expenses'))

    @api.depends('total_revenue', 'total_expenses')
    def _compute_performance_score(self):
        for record in self:
            record.performance_score = (record.total_revenue - record.total_expenses) / record.total_revenue * 100 if record.total_revenue else 0

class Branch(models.Model):
    _inherit = 'taknia.branch'

    region_id = fields.Many2one('taknia.regional.management', string='Region')