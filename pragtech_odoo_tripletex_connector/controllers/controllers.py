# -*- coding: utf-8 -*-
# from odoo import http


# class PragtechOdooTripletexConnector(http.Controller):
#     @http.route('/pragtech_odoo_tripletex_connector/pragtech_odoo_tripletex_connector', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pragtech_odoo_tripletex_connector/pragtech_odoo_tripletex_connector/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pragtech_odoo_tripletex_connector.listing', {
#             'root': '/pragtech_odoo_tripletex_connector/pragtech_odoo_tripletex_connector',
#             'objects': http.request.env['pragtech_odoo_tripletex_connector.pragtech_odoo_tripletex_connector'].search([]),
#         })

#     @http.route('/pragtech_odoo_tripletex_connector/pragtech_odoo_tripletex_connector/objects/<model("pragtech_odoo_tripletex_connector.pragtech_odoo_tripletex_connector"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pragtech_odoo_tripletex_connector.object', {
#             'object': obj
#         })

