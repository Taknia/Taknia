from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BranchScoring(models.Model):
    _name = 'branch.scoring'
    _description = 'Branch Performance Scoring'
    _rec_name = 'branch_id'

    branch_id = fields.Many2one('res.branch', string='Branch', required=True)
    scoring_date = fields.Date(string='Scoring Date', default=fields.Date.context_today, required=True)

    financial_score = fields.Float(string='Financial Performance Score', compute='_compute_financial_score', store=True)
    operational_score = fields.Float(string='Operational Efficiency Score', compute='_compute_operational_score', store=True)
    customer_satisfaction_score = fields.Float(string='Customer Satisfaction Score', required=True, default=50.0)
    employee_engagement_score = fields.Float(string='Employee Engagement Score', required=True, default=50.0)

    overall_score = fields.Float(string='Overall Branch Score', compute='_compute_overall_score', store=True)
    performance_level = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ], string='Performance Level', compute='_compute_performance_level', store=True)

    notes = fields.Text(string='Notes')

    # ----------------------------------------
    # حساب درجة الأداء المالي
    # ----------------------------------------
    @api.depends('branch_id')
    def _compute_financial_score(self):
        for record in self:
            health = self.env['branch.financial.health'].search([
                ('branch_id', '=', record.branch_id.id)
            ], order='analysis_date desc', limit=1)

            record.financial_score = health.health_score if health else 50.0

    # ----------------------------------------
    # حساب درجة الكفاءة التشغيلية
    # ----------------------------------------
    @api.depends('branch_id')
    def _compute_operational_score(self):
        for record in self:
            kpi = self.env['branch.kpi.dashboard'].search([
                ('branch_id', '=', record.branch_id.id)
            ], order='date desc', limit=1)

            if kpi:
                efficiency_score = ((kpi.revenue_growth + (100 - kpi.expense_growth)) / 2)
                record.operational_score = max(min(efficiency_score, 100), 0)
            else:
                record.operational_score = 50.0

    # ----------------------------------------
    # حساب الدرجة النهائية
    # ----------------------------------------
    @api.depends('financial_score', 'operational_score', 'customer_satisfaction_score', 'employee_engagement_score')
    def _compute_overall_score(self):
        for record in self:
            total_score = (
                (record.financial_score * 0.4) +
                (record.operational_score * 0.3) +
                (record.customer_satisfaction_score * 0.15) +
                (record.employee_engagement_score * 0.15)
            )
            record.overall_score = max(min(total_score, 100), 0)

    # ----------------------------------------
    # تحديد مستوى الأداء
    # ----------------------------------------
    @api.depends('overall_score')
    def _compute_performance_level(self):
        for record in self:
            if record.overall_score >= 85:
                record.performance_level = 'excellent'
            elif record.overall_score >= 70:
                record.performance_level = 'good'
            elif record.overall_score >= 50:
                record.performance_level = 'average'
            else:
                record.performance_level = 'poor'

    # ----------------------------------------
    # التحقق من القيم
    # ----------------------------------------
    @api.constrains('customer_satisfaction_score', 'employee_engagement_score')
    def _check_scores(self):
        for record in self:
            if not (0 <= record.customer_satisfaction_score <= 100):
                raise ValidationError(_('Customer Satisfaction Score must be between 0 and 100.'))
            if not (0 <= record.employee_engagement_score <= 100):
                raise ValidationError(_('Employee Engagement Score must be between 0 and 100.'))

    # ----------------------------------------
    # زر الوصول لتفاصيل الفرع
    # ----------------------------------------
    def action_open_branch_dashboard(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Branch Dashboard'),
            'res_model': 'branch.kpi.dashboard',
            'view_mode': 'tree,form',
            'domain': [('branch_id', '=', self.branch_id.id)],
            'context': {'default_branch_id': self.branch_id.id},
        }
