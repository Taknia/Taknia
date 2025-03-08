from odoo import models, fields

class BranchKPIDashboard(models.Model):
    _name = 'branch.kpi.dashboard'
    _description = 'Branch KPI Dashboard'

    branch_id = fields.Many2one('branch', 'Branch', required=True)
    kpi_name = fields.Char('KPI Name', required=True)
    kpi_value = fields.Float('KPI Value')
    target_value = fields.Float('Target Value')
    date = fields.Date('Date', required=True)