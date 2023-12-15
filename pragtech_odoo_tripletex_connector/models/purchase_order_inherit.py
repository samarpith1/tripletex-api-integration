from odoo import _,fields,models,api


class PurchaseOrder(models.Model):
    
    _inherit = 'purchase.order'
    _description = 'Purchase Order'
    
    tripletex_purchase_order_id = fields.Char(string='Tripletex Purchase Order Id')
   