from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    image = fields.Binary(string='Image')
    name = fields.Char(string='Name', tracking=True)
    age = fields.Integer(string='Age', compute='compute_age')
    date_of_birth = fields.Date(string='Date of Birth')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender')
    contact = fields.Char(string='Contact', tracking=True)
    ref = fields.Char(string='Reference')
    note = fields.Text(string='Note')
    active = fields.Boolean(string='Active', default=True)
    patient_tag = fields.Many2many('patient.tag', string='Tag')
    appointment_count = fields.Integer(string='Appointment Count', compute='compute_appointment_count', store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string='Appointments')
    parent = fields.Char(string='Parent')
    marital_status = fields.Selection([
        ('married','Married'),('single','Single'),
    ], string='Marital Status')
    checkup_date = fields.Datetime(string='Checkup Date')
    partner_name = fields.Char(string='Partner Name')
    is_birthday = fields.Boolean(string='Is Birhtday', compute='_compute_is_birthday')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    website = fields.Char(string='Website')


    @api.depends('appointment_ids')
    def compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    # override create method
    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals)

    # override write method
    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).write(vals)

    # copy method (project)
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (copy)") % (self.name)
        return super(HospitalPatient, self).copy(default)

    # add smart button
    def action_view_appointment(self):
        return {
            'name': _('Appointment'),
            'view_mode': 'list,form',
            'res_model': 'hospital.appointment',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'context': {},
            'domain' : [('patient_id', '=', self.id)]
        }

    # python contrains
    # @api.constrains
    # def check_age(self):
    #     for rec in self:
    #         if not rec.note:
    #             raise ValidationError(_('Note Must Full Fill'))

    # name get function
    def name_get(self):
        # patient_list = []
        # for rec in self:
        #     name = rec.ref +' '+ rec.name
        #     patient_list.append((rec.id,name))
        # return patient_list
        return [(record.id, "%s : %s" % (record.ref, record.name)) for record in self]

    @api.onchange('date_of_birth')
    def compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday




class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_user = fields.Many2one('res.users', string='Confirmed By')

    # inherit function
    def action_confirm(self):
        self.confirmed_user = self.env.user.id
        super(SaleOrder, self).action_confirm()
