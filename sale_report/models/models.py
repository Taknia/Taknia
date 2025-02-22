from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'  # توريث من النموذج الأصلي

    car_type = fields.Char(string="Car Type")
    car_license_plate_no = fields.Char(string="License Plate Number")
    car_model = fields.Integer(string="Model Year")
    car_color = fields.Char(string="Car Color")
