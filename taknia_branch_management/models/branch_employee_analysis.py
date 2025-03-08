from odoo import models, fields

class BranchEmployeeAnalysis(models.Model):
    _name = 'branch.employee.analysis'
    _description = 'Branch Employee Analysis'

    branch_id = fields.Many2one('branch', 'Branch', required=True)
    employee_id = fields.Many2one('hr.employee', 'Employee', required=True)
    analysis_data = fields.Text('Analysis Data')
    date = fields.Date('Date', required=True)