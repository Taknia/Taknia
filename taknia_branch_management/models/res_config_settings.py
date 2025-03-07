# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # إعدادات تكامل البنك
    default_integration_type = fields.Selection(
        [("import", "Import"), ("export", "Export")],
        string="Default Integration Type",
        default="import",
        help="تحديد نوع التكامل الافتراضي بين النظام والبنك (استيراد أو تصدير)."
    )

    # إعدادات التكامل مع Google Sheets
    google_sheets_integration = fields.Boolean(
        string="Enable Google Sheets Integration",
        default=False,
        help="تمكين التكامل مع Google Sheets لتمكين مزامنة البيانات."
    )

    # إعدادات التكامل مع Power BI
    power_bi_integration = fields.Boolean(
        string="Enable Power BI Integration",
        default=False,
        help="تمكين التكامل مع Power BI لتمكين تقارير الأداء والتصور البياني."
    )

    # إعدادات تكامل الفروع مع البنك
    branch_bank_integration = fields.Boolean(
        string="Enable Branch Bank Integration",
        default=True,
        help="تمكين تكامل البنك مع الفروع لإدارة الحسابات البنكية."
    )

    # إعدادات الوضع الليلي (Night Mode)
    night_mode_enabled = fields.Boolean(
        string="Enable Night Mode",
        default=False,
        help="تمكين الوضع الليلي لتقليل شدة الضوء في واجهة المستخدم."
    )

    # إعدادات تخصيص صلاحيات الفروع
    branch_permission_enabled = fields.Boolean(
        string="Enable Branch Permissions",
        default=True,
        help="تمكين تخصيص صلاحيات الفروع لكل مستخدم."
    )

    # إضافة إعدادات تكامل البنك الافتراضية
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        # الحصول على الإعدادات الافتراضية من النظام
        res.update(
            default_integration_type=self.env['ir.config_parameter'].sudo().get_param('taknia_branch_management.default_integration_type'),
            google_sheets_integration=self.env['ir.config_parameter'].sudo().get_param('taknia_branch_management.google_sheets_integration') == 'True',
            power_bi_integration=self.env['ir.config_parameter'].sudo().get_param('taknia_branch_management.power_bi_integration') == 'True',
            branch_bank_integration=self.env['ir.config_parameter'].sudo().get_param('taknia_branch_management.branch_bank_integration') == 'True',
            night_mode_enabled=self.env['ir.config_parameter'].sudo().get_param('taknia_branch_management.night_mode_enabled') == 'True',
            branch_permission_enabled=self.env['ir.config_parameter'].sudo().get_param('taknia_branch_management.branch_permission_enabled') == 'True',
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        # حفظ الإعدادات في النظام
        self.env['ir.config_parameter'].sudo().set_param('taknia_branch_management.default_integration_type', self.default_integration_type)
        self.env['ir.config_parameter'].sudo().set_param('taknia_branch_management.google_sheets_integration', str(self.google_sheets_integration))
        self.env['ir.config_parameter'].sudo().set_param('taknia_branch_management.power_bi_integration', str(self.power_bi_integration))
        self.env['ir.config_parameter'].sudo().set_param('taknia_branch_management.branch_bank_integration', str(self.branch_bank_integration))
        self.env['ir.config_parameter'].sudo().set_param('taknia_branch_management.night_mode_enabled', str(self.night_mode_enabled))
        self.env['ir.config_parameter'].sudo().set_param('taknia_branch_management.branch_permission_enabled', str(self.branch_permission_enabled))

