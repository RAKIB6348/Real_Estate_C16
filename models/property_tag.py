from odoo import api, fields, models

class PropertyType(models.Model):
    _name = 'real.estate.property.tag'
    _description = 'Real Estate Property Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')