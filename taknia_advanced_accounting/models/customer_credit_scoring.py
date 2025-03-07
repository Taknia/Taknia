from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class CustomerCreditScoring(models.Model):
    _name = 'customer.credit.scoring'
    _description = 'Customer Credit Scoring'
    
    partner_id = fields.Many2one('res.partner', string="Customer", required=True, domain=[('customer_rank', '>', 0)])
    score = fields.Float(string="Credit Score", readonly=True)
    risk_level = fields.Selection([
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk')
    ], string="Risk Level", readonly=True)
    last_evaluation_date = fields.Datetime(string="Last Evaluation Date")

    def action_evaluate_credit_score(self):
        for record in self:
            record._calculate_credit_score()

    def _calculate_credit_score(self):
        """ Calculate credit score based on customer payment history, overdue, and total transactions. """
        self.ensure_one()

        # Fetch customer invoices & payments
        invoices = self.env['account.move'].search([
            ('partner_id', '=', self.partner_id.id),
            ('move_type', 'in', ['out_invoice', 'out_refund']),
            ('state', '=', 'posted')
        ])
        
        if not invoices:
            self.score = 0
            self.risk_level = 'high'
            self.last_evaluation_date = fields.Datetime.now()
            _logger.warning(f"No financial data for customer {self.partner_id.name}")
            return

        total_invoices = len(invoices)
        paid_invoices = len(invoices.filtered(lambda inv: inv.payment_state == 'paid'))
        overdue_invoices = len(invoices.filtered(lambda inv: inv.payment_state == 'not_paid' and inv.invoice_date_due and inv.invoice_date_due < fields.Date.today()))

        # Basic Scoring Formula
        payment_ratio = (paid_invoices / total_invoices) * 100
        overdue_ratio = (overdue_invoices / total_invoices) * 100

        # Credit Score Formula (Customizable based on business needs)
        score = max(0, (payment_ratio - (overdue_ratio * 1.5)))

        # Classify risk level
        risk_level = 'low'
        if score < 40:
            risk_level = 'high'
        elif score < 70:
            risk_level = 'medium'

        # Update fields
        self.score = score
        self.risk_level = risk_level
        self.last_evaluation_date = fields.Datetime.now()

        _logger.info(f"Credit Score for {self.partner_id.name}: {score} - Risk: {risk_level}")

        return True

    @api.model
    def automated_credit_evaluation(self):
        """ Scheduled action to update credit scores for all customers automatically. """
        customers = self.search([])
        for customer in customers:
            try:
                customer._calculate_credit_score()
            except Exception as e:
                _logger.error(f"Failed to calculate credit score for {customer.partner_id.name}: {str(e)}")

