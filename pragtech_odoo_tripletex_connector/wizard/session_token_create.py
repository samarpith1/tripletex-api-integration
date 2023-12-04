
from odoo import fields,api, models,_
import requests
from odoo.exceptions import UserError


class SessionTokenWizard(models.TransientModel):
    _name = 'token.wizard'
    _description = "token.wizard here is a wizard"

    consumer_token = fields.Char(string="Consumer Token", readonly=True)
    employee_token = fields.Char(string="Employee Token", readonly=True)
    expire_date = fields.Date()


    def fetch_tokens(self):
        active_id = self.env.context.get('active_id')

        if active_id:
            company_record = self.env['res.company'].browse(active_id)
            self.consumer_token = company_record.consumer_token
            self.employee_token = company_record.employee_token
        else:
            pass


    def tripletex_token_generate(self):
        base_url = 'http://api.tripletex.io/v2'
        self.fetch_tokens()
        consumer_token = self.consumer_token
        employee_token = self.employee_token
        expiration_date = self.expire_date
        date = expiration_date.strftime('%Y-%m-%d')
        params = {'consumerToken': consumer_token, 'employeeToken': employee_token, 'expirationDate': date}

        r = requests.put(f'{base_url}/token/session/:create', params=params)
        token = self.env['res.company'].search([])
        if r.status_code == 200:
            response_data = r.json()
            if token:
                token.write({
                        'token': response_data['value']['token']
                    })
            else:
                self.env['tripletex.token'].create({
                    'expire_date': response_data['value']['expirationDate'],
                    'token': response_data['value']['token']
                })
        else:
            raise UserError(_("Not Valid"))

