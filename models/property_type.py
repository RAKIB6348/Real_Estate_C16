from odoo import api, fields, models

class PropertyType(models.Model):
    _name = 'real.estate.property.type'
    _description = 'Real Estate Property Type'

    name = fields.Char(string='Name', required=True)