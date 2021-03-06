import re
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
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    service_date = fields.Date('Date', default=datetime.now(), required=True)
    vehicle_make_id = fields.Many2one('vehicle.make', string="Vehicle Make", required=True)
    vehicle_model_id = fields.Many2one('vehicle.model', string='Vehicle Model', required=True)
    registration_no = fields.Char('Registration No', store=True, required=True)
    odometer = fields.Integer('Odometer Reading (Km)', store=True, required=True)
    service_line_ids = fields.One2many('service.line', 'service_invoice')
    state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('ready', 'Ready'), ('paid', 'Paid'), ('closed', 'Closed')], default='draft', store=True)
    paid_timestamp = fields.Date('Date', default=datetime.now())
    total = fields.Float(compute='compute_total', string='Grand Total', store=True)

    @api.constrains('registration_no')
    def _check_registration_no(self):
        reg_no_regex = r'^([a-zA-Z]){2}[\s]*\d{2}[\s]*([a-zA-z]){2}[\s]*\d{4}$'
        for record in self:
            if not re.match(reg_no_regex, record.registration_no):
                raise ValidationError(_("Vehicle registration number should be in GJ 01 RW 3534"))

    @api.one
    def action_draft(self):
        self.write({'state': 'draft'})

    @api.one
    def action_open(self):
        self.write({'state': 'open'})

    @api.one
    def action_ready(self):
        self.write({'state': 'ready'})

    @api.one
    def action_paid(self):
        self.write({'state': 'paid'})

    @api.one
    def action_close(self):
        self.write({'state': 'closed'})

    @api.depends('service_line_ids', 'vehicle_model_id')
    def compute_total(self):
        sub_total = 0
        for line in self.service_line_ids:
            sub_total += line.subtotal
        self.total = sub_total

    @api.model
    def create(self, vals):
        import pdb
        pdb.set_trace()
        vals.update({'service_record_no': self.env['ir.sequence'].next_by_code('customer.invoice')})
        return super(VehiclesService, self).create(vals)

    @api.multi
    def unlink(self):
        for invoice in self:
            if invoice.state == "closed":
                raise Warning(_('You can not delete paid and closed Services !'))
        return super(vehicle.service, self).unlink()
