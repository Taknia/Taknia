from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class BranchESGAnalysis(models.Model):
    _name = 'branch.esg.analysis'
    _description = 'Branch ESG Analysis'
    _rec_name = 'branch_id'

    branch_id = fields.Many2one('res.branch', string='Branch', required=True)
    environmental_score = fields.Float(string='Environmental Score', required=True,
                                       help='Environmental performance score (0 to 100)')
    social_score = fields.Float(string='Social Score', required=True,
                                help='Social responsibility score (0 to 100)')
    governance_score = fields.Float(string='Governance Score', required=True,
                                    help='Corporate governance score (0 to 100)')
    total_score = fields.Float(string='Total ESG Score', compute='_compute_total_score', store=True)
    analysis_date = fields.Date(string='Analysis Date', default=fields.Date.context_today, required=True)
    notes = fields.Text(string='Notes')

    @api.depends('environmental_score', 'social_score', 'governance_score')
    def _compute_total_score(self):
        for record in self:
            record.total_score = (record.environmental_score + record.social_score + record.governance_score) / 3

    @api.constrains('environmental_score', 'social_score', 'governance_score')
    def _check_scores_range(self):
        for record in self:
            if not (0 <= record.environmental_score <= 100):
                raise ValidationError(_('Environmental Score must be between 0 and 100.'))
            if not (0 <= record.social_score <= 100):
                raise ValidationError(_('Social Score must be between 0 and 100.'))
            if not (0 <= record.governance_score <= 100):
                raise ValidationError(_('Governance Score must be between 0 and 100.'))

    def action_view_branch_dashboard(self):
        """ زر يرجعني على لوحة مؤشرات الأداء للفرع المختار. """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Branch Dashboard'),
            'res_model': 'branch.kpi.dashboard',
            'view_mode': 'tree,form',
            'domain': [('branch_id', '=', self.branch_id.id)],
            'context': {'default_branch_id': self.branch_id.id},
        }
