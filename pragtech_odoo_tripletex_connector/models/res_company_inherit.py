from odoo import _, models, fields
from odoo.exceptions import UserError
import requests
import datetime
from dateutil.parser import parse
import base64

class ResCompany(models.Model):

    _inherit = 'res.company'
    _description = 'res.company'

 
    consumer_token = fields.Char()
    employee_token = fields.Char()
    token =  fields.Char(string='Token',)



    def tripletex_import_contacts(self):
        url = 'https://api.tripletex.io/v2/contact'
        consumer_token = self.consumer_token  
        employee_token = self.employee_token
        company_id = '12841878'
        session_token = self.token

        auth_token = f'{company_id}:{session_token}'
        encoded_token = base64.b64encode(auth_token.encode('utf-8')).decode('utf-8')
        print("::::::::::::::::::::::::::::::::::::::::::::::ENCODED TOKEN:::::::::::::::::::::::::::::::::::::::::::",encoded_token)

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Basic {encoded_token}',
            'consumerToken': consumer_token,
            'employeeToken': employee_token
        }

        try:
            response = requests.get(url, headers=headers)
            print("::::::::::::::::::::::::::::::::::::RESPONSE::::::::::::::::::::::::::::::::::::::::",response)
            token = self.env['res.partner'].search([])
            print("::::::::::::::::::::::::::::::::::::TOKEN SEARCH:::::::::::::::::::::::::::::::::::::::::::",token)
            if response.status_code == 200:
                json_data = response.json()
                print("::::::::::::::::::::::::::::::::::::::JSON::::::::::::::::::::::::::::::::::::::::::::::::",json_data)
                if token:
                    print("::::::::::::::::::::::::::::::::::::::SUCCESS TOKEN IF::::::::::::::::::::::::::::::::::::::::::::::::")
                    token.create({
                            'mobile': json_data['values']['phoneNumberMobile']
                        })
                else:
                    print("::::::::::::::::::::::::::::::::::::::SUCCESS TOKEN IF-ELSE::::::::::::::::::::::::::::::::::::::::::::::::")
                    print(f"Error: {response.status_code}, {response.text}")
            else:
                print("::::::::::::::::::::::::::::::::::::::RESPONSE ELSE::::::::::::::::::::::::::::::::::::::::::::::::")
                pass

        except Exception as e:
            print(f"Error during request: {e}")

    
