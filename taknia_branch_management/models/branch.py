from odoo import models, fields

class Branch(models.Model):
    _name = 'taknia.branch'
    _description = 'Branch Management'

    name = fields.Char(string='Branch Name', required=True)
    code = fields.Char(string='Branch Code', required=True)
    manager_id = fields.Many2one('res.users', string='Branch Manager')
    region = fields.Char(string='Region')
    budget = fields.Float(string='Budget')
    revenue = fields.Float(string='Revenue')
    expenses = fields.Float(string='Expenses')
    company_id = fields.Many2one('res.company', string='Company', required=True)
    active = fields.Boolean(string='Active', default=True)
    customers = fields.Many2many('res.partner', string='Customers')