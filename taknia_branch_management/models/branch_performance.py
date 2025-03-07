# -*- coding: utf-8 -*-
from odoo import models, fields, api

class BranchPerformance(models.Model):
    _name = 'branch.performance'
    _description = 'Branch Performance Tracker'

    branch_id = fields.Many2one('taknia.branch', string='Branch', required=True)
    month = fields.Date(string='Month', required=True)
    revenue = fields.Float(string='Revenue')
    expenses = fields.Float(string='Expenses')
    profit = fields.Float(string='Profit', compute='_compute_profit', store=True)

    @api.depends('revenue', 'expenses')
    def _compute_profit(self):
        for rec in self:
            rec.profit = rec.revenue - rec.expenses

    def action_generate_report(self):
        return self.env.ref('taknia_branch_management.branch_performance_action_report').report_action(self)
