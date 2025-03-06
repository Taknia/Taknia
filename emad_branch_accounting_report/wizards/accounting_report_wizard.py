from odoo import models, fields

class AccountingReportWizard(models.TransientModel):
    _name = 'accounting.report.wizard'

    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    branch_id = fields.Many2one('res.branch', string='Branch')
    partner_id = fields.Many2one('res.partner', string='Partner')
    currency_id = fields.Many2one('res.currency', string='Currency')
