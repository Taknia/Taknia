from odoo import models, fields, api

class Branch(models.Model):
    _name = 'branch.management'
    _description = 'Branch Management'

    name = fields.Char(string='Branch Name', required=True)
    code = fields.Char(string='Branch Code', required=True)
    manager = fields.Many2one('res.users', string='Branch Manager')
    location = fields.Char(string='Location')
    active = fields.Boolean(string='Active', default=True)
    # Add additional fields as necessary