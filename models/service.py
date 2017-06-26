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
    _description = 'Record of the each alighnment done in the vehicle like fornt wheel alignment'

    service_invoice = fields.Many2one('vehicle.service')
    vehicle_model = fields.Many2one('vehicle.model')
    align_position = fields.Selection([('front', 'Front'), ('rear', 'Rear')])
    wheel_balanced = fields.Integer('Total Wheel Balanced', store=True)
    weight_used_in_gms = fields.Float(string="Total Grams used", store=True)
    tyre_change_qty = fields.Integer(string='Tyre Change')
    other_service_name = fields.Char()
    other_service_charge = fields.Float(required=True, store=True)
    subtotal = fields.Float(compute="_compute_total_charge", readonly=True, store=True)

    @api.multi
    def _compute_total_charge(self):
        pass
