from odoo import models,fields,api,_

class productIinherit(models.Model):
    _inherit = "product.template"

    tripletex_product_id = fields.Char(string="Tripletex Product ID")
    cost_price_test = fields.Char(string="COST PRICE")