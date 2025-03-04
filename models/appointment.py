from odoo import api, fields, models, _
from odoo.fields import date
from odoo.fields import datetime
from odoo.exceptions import ValidationError
import random


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointment Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'patient_id'
    _order = 'id desc'

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    phone = fields.Char(string='Phone', related='patient_id.phone')
    image = fields.Binary(string='Image')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender', related='patient_id.gender')
    ref = fields.Char(string='Reference')
    appointment_date = fields.Date(string='Appointment Date', default=date.today())
    booking_date = fields.Datetime(string='Booking Date', default=datetime.now())
    prescription = fields.Html(string='Prescription')
    doctor_id = fields.Many2one('res.users', string='Doctor')
    pharmacy_lines_ids = fields.One2many('appointment.pharmacy.line', 'appointment_id', string='Pharmacy')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority", )
    state = fields.Selection([
        ('draft', "Draft"),
        ('confirm', "Confirmed"),
        ('approve', 'Approved'),
        ('canceled', "Canceled"),
    ], default='draft', string='Status', required=True)
    sl_no = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True,
                        index=True, default=lambda self: _('New'))
    progress = fields.Integer(string='Progress', compute='_compute_progress')
    duration = fields.Float(string='Duration')

    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id')


    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = random.randrange(0,30)

            elif rec.state == 'confirm':
                progress = random.randrange(30,65)

            elif rec.state == 'approve':
                progress = random.randrange(65,100)

            else:
                rec.state = 'canceled'
                progress = random.randrange(0,100)

            rec.progress = progress

    @api.model
    def create(self, vals):
        if vals.get('sl_no', _('New')) == _('New'):
            vals['sl_no'] = self.env['ir.sequence'].next_by_code('hospital.appointment', ) or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result

    # override unlink method
    def unlink(self):
        if self.state == 'approve':
            raise ValidationError(_("You cannot delete 'Approved' status!"))
        return super(HospitalAppointment, self).unlink()

    def action_draft(self):
        self.state = 'draft'

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_approve(self):
        self.state = 'approve'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Appointment Approve',
                'type': 'rainbow_man',
            }
        }

    def action_cancel(self):
        # self.state = 'canceled'
        action = self.env.ref('odoo_tutorials.action_cancel_appointment').read()[0]
        return action

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    # rainbow effect
    def action_test(self):
        # url action
        return {
            'type': 'ir.actions.act_url',
            'url': "https://www.odoo.com/",
            'target': 'new',
        }

    def action_share_whatsapp(self):
        if not self.patient_id.phone:
            raise ValidationError(_('Missing Phone number in patient record'))

        msg = 'Hi %s' % self.patient_id.name  # Fixed formatting of message
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (
        self.patient_id.phone, msg)  # Fixed URL formatting

        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_api_url,
            'target': 'new',
        }


class AppointmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.line'
    _description = 'Appointment Pharmacy Lines'

    product_id = fields.Many2one('product.product', string='Product')
    price = fields.Float(string='Price')
    qty = fields.Integer(string='Quantity')
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
    currency_id = fields.Many2one(string="Currency", related='appointment_id.currency_id')
    subtotal = fields.Monetary(string='Total', compute='_compute_subtotal_price')

    @api.depends('price', 'qty')
    def _compute_subtotal_price(self):
        for rec in self:
            rec.subtotal = rec.price * rec.qty

