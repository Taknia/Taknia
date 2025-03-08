from odoo import models, fields, api

class RegionalManagement(models.Model):
    _name = 'regional.management'
    _description = 'Regional Management'

    region_name = fields.Char(string='Region Name', required=True)
    branches = fields.One2many('branch.management', 'regional_id', string='Branches')
    manager = fields.Many2one('res.users', string='Regional Manager')
    active = fields.Boolean(string='Active', default=True)
    # Add additional fields and methods as necessary