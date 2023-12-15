from odoo import _,fields,models,api

class SaleOrder(models.Model):
    
    _inherit = 'sale.order'
    _description = 'sale.order'
    
    tripletex_sale_order_id = fields.Char(string='Tripletex Sale Order Id')



