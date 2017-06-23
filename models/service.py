# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api


class ServiceInvoice(models.Model):
    _name = 'service.invoice'
    _description = 'invoices for the serviced Vehicles'

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
    state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('ready', 'Ready'), ('paid', 'Paid')], default='draft')
    paid_timestamp = fields.Date('Date', default=datetime.now())

    @api.model
    def create(self, vals):
        vals.update({'service_record_no': self.env['ir.sequence'].get('customer.invoice')})
        return super(customer, self).create(vals)


class ServiceAlignmentLine(models.Model):
    _name = 'service.alignment.line'
    _description = 'Record of the each alighnment done in the vehicle like fornt wheel alignment'

    @api.depends('align_position')
    def _compute_total_charge(self):
        """
        Compute the amounts of the Service line.
        """
        import pdb
        pdb.set_trace()

    align_position = fields.Selection([('front', 'Front'), ('rear', 'Rear')])
    total_charge = fields.Float(compute="_compute_total_charge", readonly=True, store=True)


class ServiceWheelBalancingLine(models.Model):
    _name = 'service.wheelbalance.line'
    _description = 'reord of the each balance work done in the vehicle like fornt wheel alignment'

    @api.depends('wheel_balanced', 'weight_used_in_gms')
    def _compute_total_charge(self):
        """
        Compute the amounts of the Service line.
        """
        import pdb
        pdb.set_trace()

    wheel_balanced = fields.Integer('Total Wheel Balanced', store=True)
    weight_used_in_gms = fields.Float(string="Total Grams used", store=True)
    total_charge = fields.Float(compute="_compute_total_charge", readonly=True, store=True)
