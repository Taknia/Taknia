from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    branch_management_module_installed = fields.Boolean(string="Branch Management Module Installed", default=True)
    # Add additional fields and methods as necessary