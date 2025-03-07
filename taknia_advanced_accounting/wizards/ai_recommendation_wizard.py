from odoo import models, fields, api

class AIRecommendationWizard(models.TransientModel):
    _name = 'ai.recommendation.wizard'
    _description = 'AI Financial Recommendation Wizard'

    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    branch_id = fields.Many2one('res.branch', string='Branch')
    recommendation_type = fields.Selection([
        ('cost_cut', 'Cost Cutting'),
        ('profit_boost', 'Profit Boost'),
        ('risk_reduce', 'Risk Reduction'),
    ], string='Recommendation Type', required=True)

    def action_generate_recommendations(self):
        ai_service = self.env['ai.recommendation']
        recommendations = ai_service.generate_ai_recommendations(
            self.date_from,
            self.date_to,
            self.branch_id.id,
            self.recommendation_type
        )
        return {
            'name': 'AI Recommendations',
            'type': 'ir.actions.act_window',
            'res_model': 'ai.recommendation',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', recommendations.ids)],
        }
