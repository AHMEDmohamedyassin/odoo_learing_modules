from odoo import http
from odoo.http import request

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
            request.make_json_response({
                'message' : error
            } , status=400)