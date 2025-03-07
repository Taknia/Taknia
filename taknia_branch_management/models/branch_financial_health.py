from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class BranchFinancialHealth(models.Model):
    _name = 'branch.financial.health'
    _description = 'Branch Financial Health'
    _rec_name = 'branch_id'

    branch_id = fields.Many2one('res.branch', string='Branch', required=True)
    analysis_date = fields.Date(string='Analysis Date', default=fields.Date.context_today, required=True)
    revenue = fields.Float(string='Revenue', required=True)
    expenses = fields.Float(string='Expenses', required=True)
    net_profit = fields.Float(string='Net Profit', compute='_compute_net_profit', store=True)
    current_ratio = fields.Float(string='Current Ratio', required=True, help="Current Assets / Current Liabilities")
    debt_to_equity = fields.Float(string='Debt to Equity', required=True, help="Total Liabilities / Shareholders Equity")
    profit_margin = fields.Float(string='Profit Margin', compute='_compute_profit_margin', store=True)
    health_score = fields.Float(string='Financial Health Score', compute='_compute_health_score', store=True)
    risk_level = fields.Selection([
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk')
    ], string='Risk Level', compute='_compute_risk_level', store=True)

    notes = fields.Text(string='Notes')

    @api.depends('revenue', 'expenses')
    def _compute_net_profit(self):
        for record in self:
            record.net_profit = record.revenue - record.expenses

    @api.depends('revenue', 'net_profit')
    def _compute_profit_margin(self):
        for record in self:
            record.profit_margin = (record.net_profit / record.revenue) * 100 if record.revenue else 0

    @api.depends('current_ratio', 'debt_to_equity', 'profit_margin')
    def _compute_health_score(self):
        for record in self:
            ratio_score = (record.current_ratio / 2) * 30  # Maximum 30 points
            debt_score = (1 - (record.debt_to_equity / 5)) * 30  # Maximum 30 points
            profit_score = (record.profit_margin / 20) * 40  # Maximum 40 points
            record.health_score = max(min(ratio_score + debt_score + profit_score, 100), 0)

    @api.depends('health_score')
    def _compute_risk_level(self):
        for record in self:
            if record.health_score >= 70:
                record.risk_level = 'low'
            elif record.health_score >= 40:
                record.risk_level = 'medium'
            else:
                record.risk_level = 'high'

    @api.constrains('current_ratio', 'debt_to_equity')
    def _check_ratios(self):
        for record in self:
            if record.current_ratio <= 0:
                raise ValidationError(_('Current Ratio must be greater than zero.'))
            if record.debt_to_equity < 0:
                raise ValidationError(_('Debt to Equity cannot be negative.'))

    def action_view_branch_dashboard(self):
        """ زر للوصول إلى لوحة التحكم الخاصة بالفرع. """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Branch Dashboard'),
            'res_model': 'branch.kpi.dashboard',
            'view_mode': 'tree,form',
            'domain': [('branch_id', '=', self.branch_id.id)],
            'context': {'default_branch_id': self.branch_id.id},
        }
