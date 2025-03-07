# -*- coding: utf-8 -*-
from odoo import models, fields, api

class TakniaBranch(models.Model):
    _name = 'taknia.branch'
    _description = 'Taknia Branch'

    name = fields.Char(string='Branch Name', required=True)
    code = fields.Char(string='Branch Code', required=True)
    manager_id = fields.Many2one('res.users', string='Branch Manager')
    company_id = fields.Many2one('res.company', string='Company', required=True)
    location = fields.Char(string='Location')
    active = fields.Boolean(default=True)

    customer_count = fields.Integer(string='Customers', compute='_compute_counts')
    employee_count = fields.Integer(string='Employees', compute='_compute_counts')
    revenue = fields.Float(string='Revenue', compute='_compute_revenue')
    expenses = fields.Float(string='Expenses', compute='_compute_expenses')

    def _compute_counts(self):
        for branch in self:
            branch.customer_count = self.env['res.partner'].search_count([('branch_id', '=', branch.id)])
            branch.employee_count = self.env['hr.employee'].search_count([('branch_id', '=', branch.id)])

    def _compute_revenue(self):
        for branch in self:
            branch.revenue = sum(self.env['account.move.line'].search([
                ('branch_id', '=', branch.id),
                ('move_id.move_type', 'in', ['out_invoice', 'out_refund'])
            ]).mapped('balance'))

    def _compute_expenses(self):
        for branch in self:
            branch.expenses = sum(self.env['account.move.line'].search([
                ('branch_id', '=', branch.id),
                ('move_id.move_type', 'in', ['in_invoice', 'in_refund'])
            ]).mapped('balance'))
