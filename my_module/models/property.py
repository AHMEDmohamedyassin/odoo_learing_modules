# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    #############################################################################
    # attributes 
    #############################################################################
    _name = 'my_module.property'
    _description = 'Real Estate Property'
    _order = 'create_date desc'
    _inherit = ['mail.thread' , 'mail.activity.mixin']
    _rec_name = 'name'  # by default the name field is the record name
    active = fields.Boolean(string='Active', default=True) # archived field



    #############################################################################
    # fields 
    #############################################################################
    ref = fields.Char(string='Reference' , default='New Property' , readonly=True)
    name = fields.Char(string='Property Name', required=True, index=True , tracking=True , translate=True)
    post_code = fields.Char(string='Postal Code', size=10 , index=True)
    description = fields.Text(string='Description', help='Detailed property description' , translate=True)
    date_availability = fields.Date(string='Available From', default=fields.Date.today())
    expected_price = fields.Float(string='Expected Price', required=True, digits=(10,2))
    selling_price = fields.Float(string='Selling Price', readonly=False, digits=(10,2)) 
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    bathrooms = fields.Integer(string='Bathrooms', default=1)
    garages = fields.Boolean(string='Has Garage', default=False)
    garden = fields.Boolean(string='Has Garden', default=False)
    garden_area = fields.Float(string='Garden Area (sqm)', digits=(10,2))
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string='Garden Orientation' , default='north')
    #state field with buttons control
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
    ], string='State', default='draft')
    expected_selling_date = fields.Date(string='Expected Selling Date' , default=fields.Date.today())
    late = fields.Boolean(default=False)
    # computed field
    diff_price = fields.Float(compute='_compute_diff_price' , store=False , readonly=False , string='Difference Price')

    #############################################################################
    # relations
    #############################################################################
    owner_id = fields.Many2one('my_module.owner' , 'Owner')
    owner_name = fields.Char(related='owner_id.name' , string='Owner Name' , readonly=False)
    owner_address = fields.Char(related='owner_id.address' , string='Owner Address' , readonly=False)


    #############################################################################
    # sql constraints ( not preferred as it is not flexible , sql validation level)
    #############################################################################
    _sql_constraints = [
        # (name of constraints , constraint function , error message),
        ('unique_name' , 'unique("name")' , 'Property name must be unique'),
    ]



    #############################################################################
    # API methods and constraints for property model validation and business logic
    #############################################################################
    @api.constrains('bedrooms' , 'bathrooms')
    def _check_bedrooms_and_bathrooms_number(self):
        for record in self:
            if record.bedrooms < 1:
                raise ValidationError('Bedrooms must be at least 1')
            if record.bathrooms < 1:
                raise ValidationError('Bathrooms must be at least 1')

    #############################################################################
    # onchange api , depends api , computed field
    ##############################################################################
    # depends api : accept view fields (simple fields) , model fields (related fields) , relation fields (related model fields)
    # depends api is commonly used with computed field
    # return true record ( recorded values in database )
    @api.depends('expected_price' , 'selling_price' , 'owner_id.phone')
    def _compute_diff_price(self):
        for rec in self:
            rec.diff_price = rec.expected_price - rec.selling_price

    # onchange api : accept view fields only (simple fields) , not accept model fields nor relation fields
    # onchange api : returns only frontend values of records ( not database values ) ( psudue values )
    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            print('expected_price changed')
            if rec.expected_price < 0:
                return {    # server side warning
                    'warning' : {
                        'type' : 'warning',
                        'title' : 'value error warning',
                        'message' : 'Expected price must be positive'
                    }
                }
    #############################################################################
    # buttons methods
    #############################################################################
    # state field with buttons control
    def make_sold_properties(self):
        for rec in self:
            self.create_property_state_history('sold')
            rec.state = 'sold'

    def change_state_to_draft(self):
        for rec in self:
            self.create_property_state_history('draft')
            rec.state = 'draft'
            # rec.write({'state':'draft'})

    def change_state_to_pending(self):
        for rec in self:
            self.create_property_state_history('pending')
            rec.state = 'pending'

    def change_state_to_sold(self):
        for rec in self:
            self.create_property_state_history('sold')
            rec.state = 'sold'

    #############################################################################
    # server action , firing wizard
    #############################################################################
    def make_sold_properties(self):
        for rec in self:
            rec.state = 'sold'

    def change_property_state_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('my_module.change_state_wizard_action')
        action['context'] = {
            'default_property_id' : self.id
        }
        return action
    
    #############################################################################
    # job cron
    #############################################################################
    def check_expected_selling_date(self):
        properties_ids = self.search([])
        for rec in properties_ids:
            if rec.expected_selling_date < fields.Date.today():
                rec.late = True

    #############################################################################
    # env action
    #############################################################################
    def env_action(self):
        # search domain
        print( self.env['my_module.property'].search([ ('state' , '=' , 'draft') ]) )

        return self.env['my_module.owner'].create({
            'name' : 'John Doe2',
            'address' : '123 Main St, Anytown, USA',
            'phone' : '1234567890',
            'property_ids' : [(4, self.id)]
        })
    
    def create_property_state_history(self , new_state , reason = ""):
        for rec in self:
            self.env['my_module.property_state_history'].create({
                'property_id' : rec.id,
                'user_id' : self.env.user.id,
                'old_state' : rec.state,
                'new_state' : new_state,
                'reason' : reason
            })

    #############################################################################
    # crud methods , handling sequence
    #############################################################################
    @api.model
    def create(self ,val):
        res = super(Property , self).create(val)

        # handling property reference sequence
        if res.ref == 'New Property':
            res.ref = self.env['ir.sequence'].next_by_code('my_module.property')

        print(f"Created property")
        return res

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False):
        res = super(Property, self)._search(args, offset, limit, order, count)
        print(f"Search results")
        return res
    
    def write(self , vals):
        res = super(Property, self).write(vals)
        print(f"Edited property")
        return res
    
    def unlink(self):
        res = super(Property, self).unlink()
        print(f"Deleted property")
        return res
    
    #############################################################################
    # smart buttons action
    #############################################################################
    # set to default and client side notification 
    def action_set_default(self):
        self.ensure_one()
        default_values = {
            'bedrooms': 2,
            'bathrooms': 1,
            'garages': False,
            'garden': False,
            'garden_area': 0.0,
            'garden_orientation': 'north',
            'expected_price': 0.0,
            'selling_price': 0.0,
        }
        self.write(default_values)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Property has been reset to default values',
                'sticky': False, # True 
                'type': 'success', # warning , danger , info
            }
        }

    # navigation
    def action_owner_navigate(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'my_module.owner',
            'view_mode': 'form',  # tree , kanban
            # 'context': {      #### used in case of creating new record by setting default value inside new record form
            #     'name': 'ahmed',
            # },
            # 'domain' : [('state', '=', 'draft')] ,   ### used to filter tree data
            'target': 'current', # new (pop up window) , inline (like wizard)
            'res_id': self.owner_id.id   # open specific user 
        }
    