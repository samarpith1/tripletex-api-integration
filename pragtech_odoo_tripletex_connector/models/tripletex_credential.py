from odoo import models, fields


class TripletexResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    consumer_token = fields.Char(string='Consumer Token',
                                 config_parameter='pragtech_odoo_tripletex_connector.consumer_token',
                                 help='Enter your Consumer Token here.')
    employee_token = fields.Char(string='Employee Token',
                                 config_parameter='pragtech_odoo_tripletex_connector.employee_token',
                                 help='Enter your Employee Token here.')
