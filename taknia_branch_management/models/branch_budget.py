# -*- coding: utf-8 -*-
from odoo import models, fields

class BranchBudget(models.Model):
    _name = 'branch.budget'
    _description = 'Branch Budget Planning'

    branch_id = fields.Many2one('taknia.branch', string='Branch', required=True)
    year = fields.Char(string='Year', required=True)
    planned_revenue = fields.Float(string='Planned Revenue')
    planned_expenses = fields.Float(string='Planned Expenses')
    notes = fields.Text(string='Notes')
