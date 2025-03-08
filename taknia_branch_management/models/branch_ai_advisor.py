from odoo import models, fields, api, _
from datetime import datetime, timedelta

class BranchAIAdvisor(models.Model):
    _name = 'taknia.branch.ai.advisor'
    _description = 'Branch AI Advisor'
    _order = 'create_date desc'
    
    name = fields.Char(compute='_compute_name', store=True)
    branch_id = fields.Many2one('taknia.branch', string='Branch', required=True)
    type = fields.Selection([
        ('financial', 'Financial Insight'),
        ('operational', 'Operational Insight'),
        ('customer', 'Customer Insight'),
        ('performance', 'Performance Insight'),
        ('predictive', 'Predictive Alert'),
    ], string='Type', required=True)
    
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Critical'),
    ], string='Priority', default='1')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('done', 'Implemented'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')
    
    summary = fields.Text(string='Summary')
    description = fields.Html(string='Detailed Analysis')
    recommendation = fields.Text(string='Recommendation')
    impact_score = fields.Float(string='Impact Score')
    
    # Metrics
    current_value = fields.Float(string='Current Value')
    target_value = fields.Float(string='Target Value')
    trend = fields.Selection([
        ('increasing', 'Increasing'),
        ('decreasing', 'Decreasing'),
        ('stable', 'Stable'),
    ], string='Trend')
    
    # Tracking
    create_date = fields.Datetime(string='Generated On')
    implemented_date = fields.Datetime(string='Implemented On')
    user_id = fields.Many2one('res.users', string='Assigned To')
    
    @api.depends('type', 'branch_id', 'create_date')
    def _compute_name(self):
        for record in self:
            if record.create_date:
                date_str = fields.Datetime.to_string(record.create_date)
                record.name = f"{record.branch_id.name} - {record.type} - {date_str}"
            else:
                record.name = f"{record.branch_id.name} - {record.type}"
    
    def generate_insights(self):
        """Generate AI-powered insights for branches"""
        branches = self.env['taknia.branch'].search([('active', '=', True)])
        for branch in branches:
            self._generate_financial_insights(branch)
            self._generate_operational_insights(branch)
            self._generate_customer_insights(branch)
            self._generate_predictive_alerts(branch)
    
    def _generate_financial_insights(self, branch):
        """Generate financial insights based on branch performance"""
        if branch.actual_revenue < branch.revenue_target * 0.8:
            self.create({
                'branch_id': branch.id,
                'type': 'financial',
                'priority': '2',
                'summary': 'Revenue significantly below target',
                'description': f'Current revenue ({branch.actual_revenue}) is below 80% of target ({branch.revenue_target})',
                'recommendation': 'Review pricing strategy and marketing campaigns',
                'impact_score': 0.8,
                'current_value': branch.actual_revenue,
                'target_value': branch.revenue_target,
                'trend': 'decreasing' if branch.profit_margin < 0 else 'stable',
            })
    
    def _generate_operational_insights(self, branch):
        """Generate operational insights based on branch efficiency"""
        pass  # To be implemented
    
    def _generate_customer_insights(self, branch):
        """Generate customer-related insights"""
        pass  # To be implemented
    
    def _generate_predictive_alerts(self, branch):
        """Generate predictive alerts based on trends"""
        pass  # To be implemented
