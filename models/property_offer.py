from odoo import api, fields, models
from datetime import timedelta

# class TransientOffer(models.TransientModel):
#     _name = 'transient.model.offer'
#     _description = 'Abstact Offer'
#     _transient_max_count = 0

    # partner_email = fields.Char(string='Email')
    # partner_phone = fields.Char(string='Phone')


# abstract model e security add kora lage nah
class AbstactOffer(models.AbstractModel):
    _name = 'abstract.model.offer'
    _description = 'Abstact Offer'

    partner_email = fields.Char(string='Email')
    partner_phone = fields.Char(string='Phone')


class PropertyOffer(models.Model):
    _name = 'real.estate.property.offer'
    _inherit = ['abstract.model.offer']
    _description = 'Real Estate Property Offer'

    @api.depends('property_id','partner_id')
    def compute_name(self):
        for rec in self:
            if rec.property_id and rec.partner_id:
                rec.name = f"{rec.property_id.name} - {rec.partner_id.name}"
            else:
                rec.name = False


    name = fields.Char(string='Description', compute='compute_name')
    price = fields.Float(string='Price')
    status = fields.Selection([('accepted','Accepted'),
                               ('refused','Refused'),
                               ],string='Status')
    partner_id = fields.Many2one('res.partner', string='Customer')
    property_id = fields.Many2one('real.estate.property', string='Property')
    validity = fields.Integer(string='Validity')
    deadline = fields.Date(string='Deadline', compute='compute_deadline', inverse='inverse_deadline')
    create_date = fields.Date(string='Create Date')


    @api.onchange('validity','create_date')
    def compute_deadline(self):
        for rec in self:
            if rec.create_date:
                rec.deadline = rec.create_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False


    # inverse function
    def inverse_deadline(self):
        for rec in self:
            rec.validity = (rec.deadline - rec.create_date).days


    # create method
    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            if not rec.get('create_date'):
                rec['create_date'] = fields.Date.today()
        return super(PropertyOffer, self).create(vals)


    def action_accept_offer(self):
        self.status = 'accepted'

    def action_cancel_offer(self):
        self.status = 'refused'

