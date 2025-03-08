from odoo import models, fields, api

class BranchKPIDashboard(models.Model):
    _name = 'branch.kpi.dashboard'
    _description = 'Branch KPI Dashboard'

    branch_id = fields.Many2one('branch.management', string='Branch', required=True)
    kpi_data = fields.Text(string='KPI Data')  # Add fields to store and display KPI data

    # Add additional fields and methods as necessary