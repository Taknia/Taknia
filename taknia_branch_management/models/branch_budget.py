from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class BranchBudget(models.Model):
    _name = 'taknia.branch.budget'
    _description = 'Branch Budget'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(compute='_compute_name', store=True)
    branch_id = fields.Many2one('taknia.branch', string='Branch', required=True)
    year = fields.Integer(string='Budget Year', required=True, default=lambda self: fields.Date.today().year)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', tracking=True)
    
    currency_id = fields.Many2one('res.currency', related='branch_id.currency_id')
    
    # Budget Lines
    total_budget = fields.Monetary(string='Total Budget', currency_field='currency_id', compute='_compute_totals')
    remaining_budget = fields.Monetary(string='Remaining Budget', currency_field='currency_id', compute='_compute_remaining')
    
    line_ids = fields.One2many('taknia.branch.budget.line', 'budget_id', string='Budget Lines')
    
    # Approvals
    submitted_by = fields.Many2one('res.users', string='Submitted By')
    approved_by = fields.Many2one('res.users', string='Approved By')
    approval_date = fields.Date(string='Approval Date')
    notes = fields.Text(string='Notes')
    
    @api.depends('branch_id', 'year')
    def _compute_name(self):
        for record in self:
            record.name = f"{record.branch_id.name} - Budget {record.year}"
    
    @api.depends('line_ids.amount')
    def _compute_totals(self):
        for record in self:
            record.total_budget = sum(record.line_ids.mapped('amount'))
    
    @api.depends('total_budget', 'line_ids.spent_amount')
    def _compute_remaining(self):
        for record in self:
            total_spent = sum(record.line_ids.mapped('spent_amount'))
            record.remaining_budget = record.total_budget - total_spent
    
    def action_submit(self):
        self.write({
            'state': 'submitted',
            'submitted_by': self.env.user.id,
        })
    
    def action_approve(self):
        self.write({
            'state': 'approved',
            'approved_by': self.env.user.id,
            'approval_date': fields.Date.today(),
        })
    
    def action_reject(self):
        self.write({'state': 'rejected'})
    
    def action_reset_to_draft(self):
        self.write({'state': 'draft'})

class BranchBudgetLine(models.Model):
    _name = 'taknia.branch.budget.line'
    _description = 'Branch Budget Line'
    
    budget_id = fields.Many2one('taknia.branch.budget', string='Budget', required=True)
    category = fields.Selection([
        ('operational', 'Operational Expenses'),
        ('marketing', 'Marketing'),
        ('personnel', 'Personnel'),
        ('maintenance', 'Maintenance'),
        ('inventory', 'Inventory'),
        ('utilities', 'Utilities'),
        ('other', 'Other'),
    ], string='Category', required=True)
    
    name = fields.Char(string='Description', required=True)
    amount = fields.Monetary(string='Budgeted Amount', currency_field='currency_id', required=True)
    spent_amount = fields.Monetary(string='Spent Amount', currency_field='currency_id', compute='_compute_spent')
    currency_id = fields.Many2one('res.currency', related='budget_id.currency_id')
    
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    notes = fields.Text(string='Notes')
    
    @api.depends('budget_id.branch_id', 'category', 'start_date', 'end_date')
    def _compute_spent(self):
        for record in self:
            # To be implemented: Calculate actual spent amount from account moves
            record.spent_amount = 0.0
    
    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError(_('End date must be after start date'))
