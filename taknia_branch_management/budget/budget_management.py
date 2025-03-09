from odoo import models, fields, api

class BranchBudget(models.Model):
    _name = 'taknia.branch.budget'
    _description = 'Branch Budget Management'

    branch_id = fields.Many2one('taknia.branch', string='Branch', required=True)
    budget = fields.Float(string='Allocated Budget', required=True)
    expenses = fields.Float(string='Total Expenses', compute='_compute_expenses', store=True)
    remaining_budget = fields.Float(string='Remaining Budget', compute='_compute_remaining_budget', store=True)
    over_budget = fields.Boolean(string='Over Budget', compute='_compute_over_budget', store=True)

    @api.depends('branch_id')
    def _compute_expenses(self):
        for record in self:
            record.expenses = sum(self.env['taknia.branch.expense'].search([('branch_id', '=', record.branch_id.id)]).mapped('amount'))

    @api.depends('budget', 'expenses')
    def _compute_remaining_budget(self):
        for record in self:
            record.remaining_budget = record.budget - record.expenses

    @api.depends('remaining_budget')
    def _compute_over_budget(self):
        for record in self:
            record.over_budget = record.remaining_budget < 0

    def send_over_budget_alert(self):
        over_budget_branches = self.search([('over_budget', '=', True)])
        for branch in over_budget_branches:
            message = f"Alert: Branch {branch.branch_id.name} has exceeded its budget!"
            self.env['mail.message'].create({
                'subject': "Over Budget Alert",
                'body': message,
                'message_type': 'notification',
                'subtype_id': self.env.ref('mail.mt_note').id,
            })