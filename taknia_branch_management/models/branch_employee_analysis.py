from odoo import models, fields, api
from collections import defaultdict

class BranchEmployeeAnalysis(models.Model):
    _name = 'branch.employee.analysis'
    _description = 'Branch Employee Performance Analysis'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Analysis Name', required=True, default='New Employee Analysis', tracking=True)
    branch_id = fields.Many2one('res.branch', string='Branch', required=True, tracking=True)
    analysis_date = fields.Date(string='Analysis Date', default=fields.Date.today, tracking=True)

    total_employees = fields.Integer(string='Total Employees', compute='_compute_employee_metrics', store=True, tracking=True)
    top_performers = fields.Text(string='Top Performers', compute='_compute_employee_metrics', store=True, tracking=True)
    low_performers = fields.Text(string='Low Performers', compute='_compute_employee_metrics', tracking=True)
    avg_performance_score = fields.Float(string='Average Performance Score', compute='_compute_employee_metrics', store=True, tracking=True)

    performance_data = fields.Text(string='Detailed Performance Data', compute='_compute_employee_metrics', tracking=True)

    @api.depends('branch_id')
    def _compute_employee_metrics(self):
        for record in self:
            if not record.branch_id:
                record.total_employees = 0
                record.top_performers = ''
                record.low_performers = ''
                record.avg_performance_score = 0.0
                record.performance_data = ''
                continue

            employees = self.env['hr.employee'].search([('branch_id', '=', record.branch_id.id)])
            record.total_employees = len(employees)

            if not employees:
                record.top_performers = 'No employees found.'
                record.low_performers = 'No employees found.'
                record.avg_performance_score = 0.0
                record.performance_data = ''
                continue

            performance_scores = {}
            performance_lines = []
            total_score = 0

            for employee in employees:
                score = employee.performance_score or 0.0
                performance_scores[employee] = score
                performance_lines.append(f"{employee.name}: {score:.2f}")
                total_score += score

            # متوسط الأداء
            record.avg_performance_score = total_score / len(employees) if employees else 0.0

            # أعلى وأقل 5 موظفين
            sorted_performers = sorted(performance_scores.items(), key=lambda item: item[1], reverse=True)

            top_performers = "\n".join([f"{emp.name}: {score:.2f}" for emp, score in sorted_performers[:5]])
            low_performers = "\n".join([f"{emp.name}: {score:.2f}" for emp, score in sorted_performers[-5:]])

            record.top_performers = top_performers
            record.low_performers = low_performers
            record.performance_data = "\n".join(performance_lines)

    def action_refresh_analysis(self):
        self._compute_employee_metrics()
