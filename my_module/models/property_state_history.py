
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PropertyStateHistory(models.Model):
    _name = 'my_module.property_state_history'
    _description = 'Property State History'

    property_id = fields.Many2one('my_module.property' , 'Property')
    user_id = fields.Many2one('res.users' , 'User')
    old_state = fields.Char(string='Old State')
    new_state = fields.Char(string='New State')
    reason = fields.Char(string='Reason')
