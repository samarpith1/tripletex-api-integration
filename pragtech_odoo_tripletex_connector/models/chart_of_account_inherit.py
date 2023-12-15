from odoo import _,fields,models,api


class ChartofAccounts(models.Model):
    
    _inherit = 'account.account'
    _description = 'Chart of Accounts'
    
    tripletex_account_id = fields.Char(string='Tripletex Account Id')