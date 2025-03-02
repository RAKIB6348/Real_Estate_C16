from odoo import api, fields, models



class Property(models.Model):
    _name = 'real.estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string='Name',required=True)
    state = fields.Selection([('new','New'),
                              ('receive','Offer Receive'),
                              ('accepted','Offer Accepted'),
                              ('sold','Sold'),
                              ('cancel','Cancelled'),
                              ] ,string='Status', default='new')
    @api.depends('offer_ids')
    def compute_offers_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    offer_count = fields.Integer(string='Offers', compute='compute_offers_count')

    def action_view_form_property_offer(self):
        return {
            'type' : 'ir.actions.act_window',
            'name' : f"{self.name} - Offers",
            'domain' : [('property_id', '=', self.id)],
            'view_mode' : 'tree',
            'res_model' : 'real.estate.property.offer',
        }


    def action_sold(self):
        self.state = 'sold'

    def action_cancel(self):
        self.state = 'cancel'

    type_id = fields.Many2one('real.estate.property.type', string='Property Type')
    tag_ids = fields.Many2many('real.estate.property.tag', string='Property Tag')
    offer_ids = fields.One2many('real.estate.property.offer', 'property_id', string='Offers')
    description = fields.Text(string='Description')
    post_code = fields.Char(string='Postcode')
    date_available = fields.Date(string='Available From')
    expected_price = fields.Float(string='Expected Price')
    best_offer = fields.Float(string='Best Offer')
    selling_price = fields.Float(string='Selling Price')
    bedrooms = fields.Integer(string='Bedrooms')
    living_area = fields.Integer(string='Living Area(sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage', default=False)
    garden = fields.Boolean(string='Garden', default=False)
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection([('north','North'),
                                            ('south','South'),
                                            ('west', 'West'),
                                            ('east', 'East'),
                                            ], string='Garden Orientation')
    sales_id = fields.Many2one('res.users', string='Salesman')
    buyer_id = fields.Many2one('res.partner', string='Buyer', domain=[('is_company', '=', True)])
    phone = fields.Char(string='Phone', related='buyer_id.phone',)

    total_area = fields.Integer(string='Total Area', compute='compute_total_area')

    @api.onchange('living_area','garden_area')
    def compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area