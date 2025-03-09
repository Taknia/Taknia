from odoo import models, fields

class ReportWizard(models.TransientModel):
    _name = 'taknia.report.wizard'
    _description = 'Report Generation Wizard'

    report_type = fields.Selection([
        ('pdf', 'PDF'),
        ('excel', 'Excel')
    ], string='Report Format', required=True, default='pdf')

    def generate_report(self):
        if self.report_type == 'pdf':
            return self.env.ref('taknia_branch_management.branch_report_pdf').report_action(self)
        else:
            return self.env.ref('taknia_branch_management.branch_report_excel').report_action(self)