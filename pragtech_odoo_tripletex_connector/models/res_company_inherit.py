from odoo import _, models, fields
from odoo.exceptions import UserError
import requests
import datetime
from dateutil.parser import parse

class ResCompany(models.Model):

    _inherit = 'res.company'
    _description = 'res.company'

 
    consumer_token = fields.Char()
    employee_token = fields.Char()
    token =  fields.Char(string='Token',)
    
