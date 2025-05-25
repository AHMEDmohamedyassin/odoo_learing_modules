from odoo import http
from odoo.http import request
import json
import math
from urllib.parse import parse_qs
def serialize (prop):
    return {
        'id' : prop.id,
        'bedrooms' : prop.bedrooms,
        'bathrooms' : prop.bathrooms,
        'garages' : prop.garages,
        'garden' : prop.garden
    }

class PropertyApis(http.Controller):
    _base = '/api/v1'

    ##############################################
    ### get product data ###
    ##############################################
    @http.route(_base + "/<int:id>" , methods=["GET"] , type="http" , auth="none" , csrf=False)
    def get(self , id):
        try:
            # check if user pass an id
            if not id : 
                return request.make_json_response({
                    'message' : "id should be provided"
                } , status=400)

            # getting the record 
            rec = request.env['my_module.property'].sudo().browse(int(id))
            
            # checking if record exists 
            if not rec.exists() : 
                return request.make_json_response({
                    'message' : "id not found"
                } , status=400)

            # returning the data
            return request.make_json_response({
                'data' : serialize(rec)
            } , status=200)
        except Exception as error:
            return request.make_json_response({
                'message' : error
            } , status=400)

    
    ###########################################
    ### create property
    ###########################################
    @http.route(_base , methods=["POST"] , type="http" , auth="none" , csrf=False)
    def create(self):
        try:
            # Get the raw request data
            data = request.httprequest.data.decode('utf-8')
            vals = json.loads(data)

            res = request.env['my_module.property'].sudo().create(vals)

            # return data of created property if it is created
            if res : 
                return request.make_json_response(serialize(res) , status=200)

            return request.make_json_response({
                "message" : "something went wrong"
            } , status=400)
        except Exception as error : 
            return request.make_json_response({
                "message" : str(error)
            } , status=400)

    
    ###########################################
    ### update property
    ###########################################
    @http.route(_base , methods=["PUT"] , auth="none" , csrf=False , type="json")
    def update(self):
        try:
            args = request.httprequest.data.decode()
            vals = json.loads(args)

            #check if id is provided
            if not vals['id']: 
                return {
                    'status': 'error',
                    'message': 'id must be provided'
                }

            # getting property
            property = request.env['my_module.property'].sudo().browse(int(vals['id']))
            
            # check if property exists 
            if not property.exists():
                return {
                    'status': 'error',
                    'message': 'property not exists'
                }

            update_vals = {k: v for k, v in vals.items() if k != 'id'}

            # handle update
            property.write(update_vals)
            
            # return success data with updated property
            return {
                'status': 'success',
                'data': serialize(property)
            }

        except Exception as error: 
            return {
                'status': 'error',
                'message': str(error)
            }

    ###########################################
    ### search property
    ###########################################
    @http.route(_base + "/search" , methods=["GET"] , auth="none" , csrf=False , type="http")
    def search(self):
        try:
            query = parse_qs(request.httprequest.query_string.decode())

            print(query)

            # offset
            offset = 0
            limit = 10
            page = 1

            # limit 
            if query.get('limit') and int(query.get('limit')[0]) < limit:
                limit = int(query.get('limit')[0])

            # offset
            if query.get('page') and float(query.get('page')[0]) > 0:
                page = math.ceil(float(query.get('page')[0]))
                offset = (page - 1) * limit


            # searching
            searching = []

            # state
            if query.get('state'):
                searching += [ ('state' , '=' , query.get('state')[0] ) ]


            property = request.env['my_module.property'].sudo().search(searching , offset=offset , limit=limit , order='id desc')
            property_count = request.env['my_module.property'].sudo().search_count(searching)
            
            return request.make_json_response({
                'status': 'success',
                'data' : [serialize(prop) for prop in property] , 
                'page' : f'{page} / {math.ceil(property_count / limit)}' , 
                'limit' : limit ,
                'total' : property_count
            } , status=200)
        except Exception as error:
            return request.make_json_response({
                'status': 'error',
                'message': str(error)
            } , status=400)