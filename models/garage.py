# -*- coding: utf-8 -*-

from odoo import models, fields, api


class GarageCustomer(models.Model):
    _name = "garage.customers"
    _inherit = 'res.partner'


class VehiclesService(models.Model):
    _name = "vehicle.service"
    _rec_name = "registration_no"

    service_record_no = fields.Char('Service Number', store=True)
    customer = fields.Many2one('garage.customers')
    vehicle_make = fields.Many2one('vehicle.make')
    vehicle_model = fields.Many2one('vehicle.model')
    registration_no = fields.Char('Registration No', store=True)
    odometer = fields.Integer('Odometer Reading (Km)', store=True)
    balancing_lines = fields.One2many()
    alighnment_lines = fields.One2many()
    misc_service_lines - fields.One2many()
    total = fields.Float(string='Total')

    @api.model
    def create(self, vals):
        vals.update({'service_record_no': self.env['ir.sequence'].get('customer.invoice')})
        return super(customer, self).create(vals)
