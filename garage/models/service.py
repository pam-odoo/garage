# -*- coding: utf-8 -*-

import re
from datetime import datetime
from odoo import models, fields, api, _


class ServiceInvoice(models.Model):
    _name = 'service.invoice'
    _description = 'invoices for the serviced Vehicles'

    service_record_no = fields.Char('Service Number', store=True)
    service_date = fields.Date('Date', default=datetime.now())
    customer = fields.Many2one('res.partner')
    vehicle_make = fields.Many2one('vehicle.make')
    vehicle_model = fields.Many2one('vehicle.model')
    registration_no = fields.Char('Registration No', store=True)
    odometer = fields.Integer('Odometer Reading (Km)', store=True)
    total = fields.Float(string='Total')
    state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('ready', 'Ready'), ('paid', 'Paid'), ('closed', 'Closed')], default='draft')
    paid_timestamp = fields.Date('Date', default=datetime.now())

    @api.constrains('registration_no')
    def _check_registration_no(self):
        reg_no_regex = "r^([a-zA-Z]){2}[\s]*\d{2}[\s]*([a-zA-z]){2}[\s]*\d{4}"
        for record in self:
            if not re.match(reg_no_regex, record.registration_no):
                raise ValidationError("Vehicle registration number should be in GJ 01 RW 3534 format")

    @api.model
    def create(self, vals):
        vals.update({'service_record_no': self.env['ir.sequence'].get('customer.invoice')})
        return super(customer, self).create(vals)


class ServiceLine(models.Model):
    _name = 'service.line'
    _description = 'Service Work'

    service_invoice = fields.Many2one('vehicle.service')
    vehicle_model = fields.Many2one('vehicle.model')
    align_position = fields.Selection([('front', 'Front'), ('rear', 'Rear')])
    wheel_balanced = fields.Integer('Total Wheel Balanced', store=True)
    weight_used_in_gms = fields.Float(string="Total Grams used", store=True)
    tyre_change_qty = fields.Integer(string='Tyre Change')
    alignment_charge = fields.Float()
    weight_charge = fields.Float()
    wheel_balancing_charge = fields.Float()
    tyre_change_charge = fields.Float()
    other_service_name = fields.Char()
    other_service_charge = fields.Float(required=True, store=True)
    subtotal = fields.Float(compute="compute_total_charge", readonly=True, store=True)

    @api.onchange("align_position", "wheel_balanced", "weight_used_in_gms", "tyre_change_qty")
    def onchange_lines(self):
        try:
            service_charges = self.env['service.charge'].search([('vehicle_model', '=', self.service_invoice.vehicle_model_id.id)])
        except:
            raise ValidationError("Please First define charges for the selected Model")

        if self.align_position == 'front':
            self.alignment_charge = service_charges.alg_charge_front
        elif self.align_position == 'rear':
            self.alignment_charge = service_charges.alg_charge_rear
        else:
            self.alignment_charge = ''

        if self.wheel_balanced:
            self.wheel_balancing_charge = self.wheel_balanced * service_charges.balance_charge_per_tire
        else:
            self.wheel_balancing_charge = ''

        if self.weight_used_in_gms:
            self.weight_charge = self.weight_used_in_gms * service_charges.bal_charge_per_gms_used
        else:
            self.weight_charge = ''

        if self.tyre_change_qty:
            self.tyre_change_charge = self.tyre_change_qty * service_charges.charge_per_tire_change
        else:
            self.tyre_change_charge = ''

    @api.depends("align_position", "wheel_balanced", "weight_used_in_gms", "tyre_change_qty")
    def compute_total_charge(self):
        self.subtotal = (self.alignment_charge + self.wheel_balancing_charge + self.weight_charge + self.tyre_change_charge + self.other_service_charge)
