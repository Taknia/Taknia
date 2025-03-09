from odoo import models, fields, api

class BranchDashboard(models.Model):
    _name = 'taknia.branch.dashboard'
    _description = 'Branch Dashboard'

    branch_id = fields.Many2one('taknia.branch', string='Branch', required=True)
    revenue = fields.Float(string='Revenue')
    expenses = fields.Float(string='Expenses')
    budget = fields.Float(string='Budget')
    performance_score = fields.Float(string='Performance Score')
    customer_satisfaction = fields.Float(string='Customer Satisfaction (%)')

    @api.model
    def get_dashboard_data(self):
        branches = self.env['taknia.branch'].search([])
        data = []
        for branch in branches:
            data.append({
                'name': branch.name,
                'revenue': branch.revenue,
                'expenses': branch.expenses,
                'budget': branch.budget,
                'performance_score': branch.performance_score,
                'customer_satisfaction': branch.customer_satisfaction,
            })
        return data