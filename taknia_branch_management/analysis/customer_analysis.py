from odoo import models, fields, api

class CustomerAnalysis(models.Model):
    _name = 'taknia.customer.analysis'
    _description = 'Customer Profitability Analysis'

    branch_id = fields.Many2one('taknia.branch', string='Branch', required=True)
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    total_sales = fields.Float(string='Total Sales', compute='_compute_total_sales', store=True)
    total_payments = fields.Float(string='Total Payments', compute='_compute_total_payments', store=True)
    profitability = fields.Float(string='Profitability', compute='_compute_profitability', store=True)

    @api.depends('customer_id')
    def _compute_total_sales(self):
        for record in self:
            record.total_sales = sum(self.env['account.move'].search([('partner_id', '=', record.customer_id.id), ('move_type', '=', 'out_invoice')]).mapped('amount_total'))

    @api.depends('customer_id')
    def _compute_total_payments(self):
        for record in self:
            record.total_payments = sum(self.env['account.payment'].search([('partner_id', '=', record.customer_id.id)]).mapped('amount'))

    @api.depends('total_sales', 'total_payments')
    def _compute_profitability(self):
        for record in self:
            record.profitability = record.total_sales - record.total_payments