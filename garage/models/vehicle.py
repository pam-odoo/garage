# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class VehicleServiceCharge(models.Model):
    _name = 'service.charge'
    _description = 'Description'

    vehicle_make = fields.Many2one('vehicle.make')
    vehicle_model = fields.Many2one('vehicle.model')
    alg_charge_front = fields.Float('Front Alighnment Charge', default=0.0)
    alg_charge_rear = fields.Float('Rear Alighnment Charge', default=0.0)
    balance_charge_per_tire = fields.Float('Balancing Charge', default=0.0)
    bal_charge_per_gms_used = fields.Float('Balancing Weight Charge', default=0.0)
    charge_per_tire_change = fields.Float('Tyre Change Charge', default=0.0)

    _sql_constraints = [('name_uniq', 'unique(vehicle_model, vehicle_make)', _('Can not have Two different Charges for same model!'))]


class VehicleMake(models.Model):
    _name = 'vehicle.make'
    _description = 'Description'
    _rec_name = 'vehicle_make'

    vehicle_make = fields.Char(string='Brand Name/ Make',)
    country = fields.Many2one('res.country')

    _sql_constraints = [('name_uniq', 'unique(vehicle_make)', _('You have already that brand in you base!'))]


class VehicleModel(models.Model):
    _name = 'vehicle.model'
    _description = 'Model of the vehicle i.e Tiago,baleno,avantedore etc.'
    _rec_name = 'vehicle_model'

    vehicle_make = fields.Many2one('vehicle.make', string='Brand Name/ Make', required=True)
    vehicle_model = fields.Char(string='Model Name')

    _sql_constraints = [('name_uniq', 'unique(vehicle_model)', _('Can not have duplicate vehicle model!'))]
