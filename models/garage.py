# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api


class GarageCustomer(models.Model):
    _name = "res.partner"
    _inherit = 'res.partner'


class VehiclesService(models.Model):
    _name = "vehicle.service"
    _rec_name = "registration_no"

    service_record_no = fields.Char('Service Number', store=True)
    customer_id = fields.Many2one('res.partner', string='Customer')
    service_date = fields.Date('Date', default=datetime.now())
    vehicle_make_id = fields.Many2one('vehicle.make', string="Vehicle Make")
    vehicle_model_id = fields.Many2one('vehicle.model', string='Vehicle Model')
    registration_no = fields.Char('Registration No', store=True)
    odometer = fields.Integer('Odometer Reading (Km)', store=True)
    alighnment_line_ids = fields.One2many('service.alignment.line', 'service_invoice')
    balancing_line_ids = fields.One2many('service.wheelbalance.line', 'service_invoice')
    misc_service_line_ids = fields.One2many('service.misc.line', 'service_invoice')
    state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('ready', 'Ready'), ('paid', 'Paid')], default='draft')
    paid_timestamp = fields.Date('Date', default=datetime.now())
    total = fields.Float(string='Total')

    @api.model
    def create(self, vals):
        vals.update({'service_record_no': self.env['ir.sequence'].get('customer.invoice')})
        return super(VehiclesService, self).create(vals)

    @api.multi
    def _action_paid(self):
        self.ensure_one()
        self.write({'state': 'paid'})
