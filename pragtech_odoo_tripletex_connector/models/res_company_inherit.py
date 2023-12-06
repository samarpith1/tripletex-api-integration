from odoo import _, models, fields,api
from odoo.exceptions import UserError
import requests,phonenumbers
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

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Basic {encoded_token}',
            'consumerToken': consumer_token,
            'employeeToken': employee_token
        }

        try:
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                
                json_data = response.json()
                self.process_tripletex_contacts(json_data['values'])

            else:
                print(f"Error: {response.status_code}, {response.text}")

        except Exception as e:
            print(f"Error during request: {e}")
            
            
            
            
            

    @api.model
    def process_tripletex_contacts(self, tripletex_contacts):
        for contact in tripletex_contacts:
           
            partner_data = {
                'name': f"{contact.get('firstName', '')} {contact.get('lastName', '')}",
                'email': contact.get('email'),
                'mobile': str(contact.get('phoneNumberMobile', '')),
                'phone': contact.get('phoneNumberWork', ''),
                'tripletex_contact_id': contact.get('id'),
                
            }

            
            partner = self.env['res.partner'].search([('tripletex_contact_id', '=', partner_data['tripletex_contact_id'])])
            

            if partner:
               
                partner.write(partner_data)
            else:
                
                
                partner_id = self.env['res.partner'].create(partner_data)
                



    
    # @api.model
    # def create_customer_in_tripletex(self):
    #     # Assuming 'xero_oauth_token' is the Tripletex API token in your res.partner model
    #     partners = self.env['res.partner'].search([])

    #     for partner in partners:
    #         self.create_main_customer_in_tripletex(partner)
        
    #     success_form = self.env.ref('your_module.export_successfull_view', False)
    #     return {
    #         'name': _('Notification'),
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'res.company.message',
    #         'views': [(success_form.id, 'form')],
    #         'view_id': success_form.id,
    #         'target': 'new',
    #     }

    # def create_main_customer_in_tripletex(self, partner):
    #     url = 'https://tripletex.no/v2/contact'
    #     tripletex_token = partner.tripletex_api_token  # Replace with the field in res.partner containing Tripletex API token

    #     headers = {
    #         'Accept': 'application/json',
    #         'Authorization': f'Tripletex {tripletex_token}',
    #         'Content-Type': 'application/json; charset=utf-8',
    #     }

    #     # Create the payload based on your Tripletex contact structure
    #     payload = {
    #         "id": 0,
    #         "version": 0,
    #         "firstName": partner.first_name,
    #         "lastName": partner.last_name,
    #         # Add other fields as needed
    #     }

    #     try:
    #         response = requests.post(url, headers=headers, json=payload)

    #         if response.status_code == 200:
    #             # Request was successful
    #             json_data = response.json()
    #             self.process_tripletex_response(json_data)  # Implement this method to handle the response

    #         else:
    #             print(f"Error: {response.status_code}, {response.text}")

    #     except Exception as e:
    #         print(f"Error during request: {e}")

    # def process_tripletex_response(self, response):
    #     # Implement logic to handle the Tripletex API response
    #     pass
