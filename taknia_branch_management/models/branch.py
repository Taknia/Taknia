from odoo import models, fields

class Branch(models.Model):
    _name = 'branch'
    _description = 'Branch'

    name = fields.Char('Branch Name', required=True)
    code = fields.Char('Branch Code', required=True)
    manager_id = fields.Many2one('res.users', 'Branch Manager')
    address = fields.Char('Branch Address')
    phone = fields.Char('Branch Phone')
    email = fields.Char('Branch Email')
    active = fields.Boolean('Active', default=True)