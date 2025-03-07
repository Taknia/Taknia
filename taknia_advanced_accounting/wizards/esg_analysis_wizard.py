from odoo import models, fields, api

class ESGAnalysisWizard(models.TransientModel):
    _name = 'esg.analysis.wizard'
    _description = 'ESG Analysis Wizard'

    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    branch_id = fields.Many2one('res.branch', string='Branch')
    category = fields.Selection([
        ('environment', 'Environment'),
        ('social', 'Social'),
        ('governance', 'Governance'),
    ], string='Category', required=True)

    def action_run_esg_analysis(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'branch_id': self.branch_id.id,
            'category': self.category,
        }
        return self.env.ref('taknia_advanced_accounting.action_esg_analysis_report').report_action(None, data=data)
