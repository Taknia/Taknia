from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    branch_id = fields.Many2one('res.branch', string='Branch', tracking=True)
    performance_score = fields.Float(string='Performance Score', tracking=True,
                                     help='Overall employee performance score (0 to 100)',
                                     default=0.0)

    @api.constrains('performance_score')
    def _check_performance_score(self):
        for record in self:
            if record.performance_score < 0 or record.performance_score > 100:
                raise ValueError('Performance Score must be between 0 and 100.')
