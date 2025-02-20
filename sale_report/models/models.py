from odoo import models, fields

class SaleReportCustom(models.Model):
    _name = 'sale.report.custom'  # تحقق من هذا الاسم
    _description = 'Custom Sale Report'

    name = fields.Char(string="Report Name")

    car_type = fields.Char(string="Car Type")
    car_license_plate_no = fields.Char(string="License Plate Number")
    car_model = fields.Integer(string="Model Year")
    car_color = fields.Char(string="Car Color")
