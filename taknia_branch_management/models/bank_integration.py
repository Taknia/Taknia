# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging
import datetime

_logger = logging.getLogger(__name__)

class BankIntegration(models.Model):
    _name = 'taknia.branch.bank.integration'
    _description = 'Bank Integration for Branches'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # تعريف الحقول الأساسية
    name = fields.Char(string='Integration Name', required=True, track_visibility='onchange')
    branch_id = fields.Many2one('taknia.branch.management', string='Branch', required=True)
    bank_account_id = fields.Many2one('account.account', string='Bank Account', required=True)
    integration_type = fields.Selection([('import', 'Import'), ('export', 'Export')], string='Integration Type', required=True)
    last_import_date = fields.Datetime(string='Last Import Date')
    last_export_date = fields.Datetime(string='Last Export Date')
    active = fields.Boolean(string='Active', default=True)
    status = fields.Selection([
        ('idle', 'Idle'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ], string='Status', default='idle', track_visibility='onchange')

    # إنشاء سجل جديد
    @api.model
    def create(self, vals):
        record = super(BankIntegration, self).create(vals)
        _logger.info(f'Bank Integration created: {record.name}')
        return record

    # تحديث بيانات كشف الحساب البنكي
    def update_bank_statement(self):
        for record in self:
            if record.integration_type == 'import':
                # منطق استيراد كشف الحساب البنكي
                _logger.info(f'Importing bank statements for branch {record.branch_id.name}')
                # معالجة استيراد البيانات من البنك (محاكاة هنا)
                record.last_import_date = fields.Datetime.now()
                record.status = 'completed'
            elif record.integration_type == 'export':
                # منطق تصدير كشف الحساب البنكي
                _logger.info(f'Exporting bank statements for branch {record.branch_id.name}')
                # معالجة تصدير البيانات للبنك (محاكاة هنا)
                record.last_export_date = fields.Datetime.now()
                record.status = 'completed'

    # اختبار التكامل مع البنك
    def action_test_integration(self):
        for record in self:
            _logger.info(f'Testing bank integration for {record.name}')
            if not record.bank_account_id:
                raise ValidationError("Please specify a valid bank account.")
            # محاكاة اختبار الاتصال بالبنك
            _logger.info("Test completed successfully.")

    # تفعيل أو تعطيل التكامل
    def toggle_active(self):
        for record in self:
            record.active = not record.active
            _logger.info(f'Bank Integration for branch {record.branch_id.name} is now {"active" if record.active else "inactive"}')

    # إعداد التنبيهات
    def send_alert(self, message):
        # منطق إرسال التنبيهات للمستخدمين المعنيين
        _logger.info(f'Alert: {message}')
        # يمكن إرسال التنبيه عبر البريد الإلكتروني أو نظام الإشعارات في Odoo

    # إجراء العمليات التلقائية عبر Cron Jobs
    def scheduled_import_export(self):
        for record in self:
            if record.integration_type == 'import' and record.status == 'idle':
                _logger.info(f'Running scheduled import for {record.name}')
                record.update_bank_statement()
            elif record.integration_type == 'export' and record.status == 'idle':
                _logger.info(f'Running scheduled export for {record.name}')
                record.update_bank_statement()

# إعدادات التكامل مع البنك في صفحة الإعدادات
class BankIntegrationConfigSettings(models.TransientModel):
    _name = 'taknia.bank.integration.config'
    _inherit = 'res.config.settings'

    # إضافة إعدادات تكامل البنك
    default_integration_type = fields.Selection(
        [("import", "Import"), ("export", "Export")],
        string="Default Integration Type",
        default="import"
    )

    @api.model
    def get_values(self):
        res = super(BankIntegrationConfigSettings, self).get_values()
        res.update(
            default_integration_type=self.env['ir.config_parameter'].sudo().get_param('taknia_bank_integration.default_integration_type'),
        )
        return res

    def set_values(self):
        super(BankIntegrationConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('taknia_bank_integration.default_integration_type', self.default_integration_type)
