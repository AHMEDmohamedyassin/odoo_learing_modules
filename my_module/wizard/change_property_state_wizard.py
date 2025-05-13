
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ChangePropertyStateWizard(models.Model):
    _name = 'my_module.change_state_wizard'
    _description = 'Property State Change wizard'

    property_id = fields.Many2one('my_module.property' , 'Property')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
    ], string='State', default='draft')
    reason = fields.Char(string="reason")


    def action_change_state(self):
        # record data to history table
        self.property_id.create_property_state_history(self.state , self.reason)

        self.property_id.state = self.state
