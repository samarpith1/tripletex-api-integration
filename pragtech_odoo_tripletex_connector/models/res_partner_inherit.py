from odoo import _,fields,models,api


class ResContact(models.Model):
    
    _inherit = 'res.partner'
    _description = 'Res.Partner'
    
    tripletex_contact_id = fields.Char(string='Tripletex Contact Id')
    tripletex_supplier_id  = fields.Char(string='Tripletex Supplier Id')
    
    
    
        
        
    