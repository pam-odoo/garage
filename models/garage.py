# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api, _
from odoo import tools
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource


class GarageCustomer(models.Model):
    _name = "res.partner"
    _inherit = 'res.partner'


class VehiclesService(models.Model):
    _name = "vehicle.service"
    _rec_name = "registration_no"

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    image = fields.Binary("Car Image", default=_default_image, attachment=True, help="This field holds the image used as photo for the employee, limited to 1024x1024px.")
    image_medium = fields.Binary("Medium-sized photo", attachment=True, help="Medium-sized photo of the employee. It is automatically ""resized as a 128x128px image, with aspect ratio preserved. ""Use this field in form views or some kanban views.")
    image_small = fields.Binary("Small-sized photo", attachment=True, help="Small-sized photo of the employee. It is automatically ""resized as a 64x64px image, with aspect ratio preserved. ""Use this field anywhere a small image is required.")
    service_record_no = fields.Char('Service Number', store=True, required=True, copy=False, readonly=True, default=lambda self: _('New'))
    customer_id = fields.Many2one('res.partner', string='Customer')
    service_date = fields.Date('Date', default=datetime.now())
    vehicle_make_id = fields.Many2one('vehicle.make', string="Vehicle Make")
    vehicle_model_id = fields.Many2one('vehicle.model', string='Vehicle Model')
    registration_no = fields.Char('Registration No', store=True)
    odometer = fields.Integer('Odometer Reading (Km)', store=True)
    service_line_ids = fields.One2many('service.line', 'service_invoice')
    state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('ready', 'Ready'), ('paid', 'Paid')], default='draft')
    paid_timestamp = fields.Date('Date', default=datetime.now())
    total = fields.Float(compute='compute_total', string='Grand Total', store=True)

    @api.model
    def create(self, vals):
        vals.update({'service_record_no': self.env['ir.sequence'].get('customer.invoice')})
        return super(VehiclesService, self).create(vals)

    @api.multi
    def _action_paid(self):
        self.ensure_one()
        self.write({'state': 'paid'})

    @api.onchange('service_line_ids', 'vehicle_model_id')
    def compute_total(self):
        vehicle_model_id = self.vehicle_model_id
        service_charges = self.env['service.charge'].search([('vehicle_model', "=", vehicle_model_id.id)])

        if self.service_line_ids:
            lump_sum = 0.00
            for service_line in self.service_line_ids:
                if service_line.align_position == "front":
                    lump_sum += service_charges.alg_charge_front
                else:
                    lump_sum += service_charges.alg_charge_rear

                if service_line.wheel_balanced:
                    lump_sum += (service_line.wheel_balanced * service_charges.balance_charge_per_tire)
                if service_line.weight_used_in_gms:
                    lump_sum += service_line.weight_used_in_gms * (service_charges.bal_charge_per_gms_used)
                if service_line.tyre_change_qty:
                    lump_sum += (service_line.tyre_change_qty) * (service_charges.charge_per_tire_change)
                if service_line.other_service_charge:
                    lump_sum += service_line.other_service_charge
                self.total = lump_sum
