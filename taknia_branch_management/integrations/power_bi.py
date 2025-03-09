from odoo import models, fields

class PowerBIIntegration(models.Model):
    _name = 'taknia.power.bi'
    _description = 'Power BI Integration'

    report_url = fields.Char(string='Power BI Report URL', required=True)

    def open_power_bi_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': self.report_url,
            'target': 'new',
        }