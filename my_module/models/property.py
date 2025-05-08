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
    name = fields.Char(string='Property Name', required=True, index=True , tracking=True)
    post_code = fields.Char(string='Postal Code', size=10 , index=True)
    description = fields.Text(string='Description', help='Detailed property description')
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
                return {
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
            rec.state = 'sold'

    def change_state_to_draft(self):
        for rec in self:
            rec.state = 'draft'
            # rec.write({'state':'draft'})

    def change_state_to_pending(self):
        for rec in self:
            rec.state = 'pending'

    def change_state_to_sold(self):
        for rec in self:
            rec.state = 'sold'

    #############################################################################
    # server action
    #############################################################################
    def make_sold_properties(self):
        for rec in self:
            rec.state = 'sold'

    
    #############################################################################
    # job cron
    #############################################################################
    def check_expected_selling_date(self):
        properties_ids = self.search([])
        for rec in properties_ids:
            if rec.expected_selling_date < fields.Date.today():
                rec.late = True

    #############################################################################
    # crud methods
    #############################################################################
    # @api.model_create_multi
    # def create(self ,val):
    #     res = super(Property , self).create(val)
    #     print(f"Created property")
    #     return res

    # @api.model
    # def _search(self, args, offset=0, limit=None, order=None, count=False):
    #     res = super(Property, self)._search(args, offset, limit, order, count)
    #     print(f"Search results")
    #     return res
    
    # def write(self , vals):
    #     res = super(Property, self).write(vals)
    #     print(f"Edited property")
    #     return res
    
    # def unlink(self):
    #     res = super(Property, self).unlink()
    #     print(f"Deleted property")
    #     return res
    
    