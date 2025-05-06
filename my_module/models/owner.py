# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Owner(models.Model):
    # attributes 
    _name = 'my_module.owner'

    # fields 
    name = fields.Char(string='owner Name', required=True, index=True)
    phone = fields.Char()
    address = fields.Char()

    # relations
    property_ids = fields.One2many('my_module.property' , 'owner_id')
