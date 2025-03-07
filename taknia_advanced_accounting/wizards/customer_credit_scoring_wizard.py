from odoo import models, fields, api

class CustomerCreditScoringWizard(models.TransientModel):
    _name = 'customer.credit.scoring.wizard'
    _description = 'Customer Credit Scoring Wizard'

    partner_ids = fields.Many2many('res.partner', string='Customers', required=True)

    def action_calculate_credit_scores(self):
        scoring_service = self.env['customer.credit.scoring']
        scoring_service.calculate_scores(self.partner_ids)
        return {
            'name': 'Customer Credit Scores',
            'type': 'ir.actions.act_window',
            'res_model': 'customer.credit.scoring',
            'view_mode': 'tree,form',
            'domain': [('partner_id', 'in', self.partner_ids.ids)],
        }
