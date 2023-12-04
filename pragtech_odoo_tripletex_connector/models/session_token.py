from odoo import _, models, fields

class SessionToken(models.Model):

    _name = 'tripletex.session.token'
    _description = 'Session Token'

    session_token  = fields.Char()
    expiration_date =  fields.Date()
    