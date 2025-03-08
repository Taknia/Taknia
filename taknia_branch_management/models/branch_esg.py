from odoo import models, fields, api, _

class BranchESG(models.Model):
    _name = 'taknia.branch.esg'
    _description = 'Branch ESG Metrics'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(compute='_compute_name', store=True)
    branch_id = fields.Many2one('taknia.branch', string='Branch', required=True)
    date = fields.Date(string='Report Date', default=fields.Date.today, required=True)
    
    # Environmental Metrics
    energy_consumption = fields.Float(string='Energy Consumption (kWh)', tracking=True)
    renewable_energy_pct = fields.Float(string='Renewable Energy (%)', tracking=True)
    water_usage = fields.Float(string='Water Usage (m³)', tracking=True)
    waste_generated = fields.Float(string='Waste Generated (kg)', tracking=True)
    waste_recycled = fields.Float(string='Waste Recycled (%)', tracking=True)
    carbon_emissions = fields.Float(string='Carbon Emissions (tCO2e)', tracking=True)
    
    # Social Metrics
    employee_satisfaction = fields.Float(string='Employee Satisfaction Score', tracking=True)
    training_hours = fields.Float(string='Training Hours per Employee', tracking=True)
    community_programs = fields.Integer(string='Community Programs', tracking=True)
    local_employment = fields.Float(string='Local Employment (%)', tracking=True)
    diversity_score = fields.Float(string='Diversity Score', tracking=True)
    health_safety_incidents = fields.Integer(string='Health & Safety Incidents', tracking=True)
    
    # Governance Metrics
    compliance_score = fields.Float(string='Compliance Score', tracking=True)
    risk_assessment_score = fields.Float(string='Risk Assessment Score', tracking=True)
    policy_implementation = fields.Float(string='Policy Implementation Score', tracking=True)
    
    # Overall Scores
    environmental_score = fields.Float(string='Environmental Score', compute='_compute_environmental_score', store=True)
    social_score = fields.Float(string='Social Score', compute='_compute_social_score', store=True)
    governance_score = fields.Float(string='Governance Score', compute='_compute_governance_score', store=True)
    overall_esg_score = fields.Float(string='Overall ESG Score', compute='_compute_overall_score', store=True)
    
    @api.depends('branch_id', 'date')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.branch_id.name} - ESG Report {record.date}"
    
    @api.depends('energy_consumption', 'renewable_energy_pct', 'water_usage', 
                'waste_generated', 'waste_recycled', 'carbon_emissions')
    def _compute_environmental_score(self):
        for record in self:
            # Weighted average of environmental metrics
            record.environmental_score = (
                (100 - min(record.energy_consumption / 1000, 100)) * 0.3 +
                record.renewable_energy_pct * 0.2 +
                (100 - min(record.water_usage / 100, 100)) * 0.2 +
                record.waste_recycled * 0.2 +
                (100 - min(record.carbon_emissions * 10, 100)) * 0.1
            )
    
    @api.depends('employee_satisfaction', 'training_hours', 'community_programs',
                'local_employment', 'diversity_score', 'health_safety_incidents')
    def _compute_social_score(self):
        for record in self:
            # Weighted average of social metrics
            record.social_score = (
                record.employee_satisfaction * 0.25 +
                min(record.training_hours * 5, 100) * 0.2 +
                min(record.community_programs * 10, 100) * 0.2 +
                record.local_employment * 0.15 +
                record.diversity_score * 0.1 +
                (100 - min(record.health_safety_incidents * 10, 100)) * 0.1
            )
    
    @api.depends('compliance_score', 'risk_assessment_score', 'policy_implementation')
    def _compute_governance_score(self):
        for record in self:
            # Weighted average of governance metrics
            record.governance_score = (
                record.compliance_score * 0.4 +
                record.risk_assessment_score * 0.3 +
                record.policy_implementation * 0.3
            )
    
    @api.depends('environmental_score', 'social_score', 'governance_score')
    def _compute_overall_score(self):
        for record in self:
            # Equal weighting for E, S, and G components
            record.overall_esg_score = (
                record.environmental_score * 0.33 +
                record.social_score * 0.33 +
                record.governance_score * 0.34
            )
    
    def generate_esg_report(self):
        """Generate detailed ESG report in PDF format"""
        # To be implemented: PDF report generation
        pass
    
    def export_to_excel(self):
        """Export ESG data to Excel"""
        # To be implemented: Excel export functionality
        pass
