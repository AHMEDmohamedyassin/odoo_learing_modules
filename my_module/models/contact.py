# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InheritedContact(models.Model):
    _inherit = 'res.partner'

    owner_id = fields.Many2one('my_module.owner', string='Owner')
    owner_name = fields.Char(related='owner_id.name' , string='Owner Name' , readonly=False)
    owner_address = fields.Char(related='owner_id.address' , string='Owner Address' , readonly=False)
    
