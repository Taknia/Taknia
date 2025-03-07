# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AIBranchAdvisor(models.Model):
    _name = 'ai.branch.advisor'
    _description = 'AI Branch Advisor Recommendations'

    branch_id = fields.Many2one('taknia.branch', string='Branch', required=True)
    recommendation = fields.Text(string='Recommendation')
    date = fields.Date(string='Date', default=fields.Date.context_today)

    def action_apply_recommendation(self):
        # تنفيذ التوصية (Placeholder logic)
        self.ensure_one()
        if 'تخفيض المصاريف' in self.recommendation:
            # مثال: إشعار للمدير
            self.env['mail.activity'].create({
                'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                'res_id': self.branch_id.id,
                'res_model_id': self.env['ir.model']._get_id('taknia.branch'),
                'summary': 'AI Recommendation: تخفيض المصاريف',
                'user_id': self.branch_id.manager_id.id,
            })
