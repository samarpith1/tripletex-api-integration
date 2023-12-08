from odoo import _, models, fields,api
from odoo.exceptions import UserError
import requests
import datetime
from dateutil.parser import parse
import base64
import logging
_logger = logging.getLogger(__name__)

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
                


    
    
    
    
 

 

    def export_contacts_to_tripletex(self):
        try:
            

            partners = self.env['res.partner'].search([])

            for partner in partners:
            
       
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
                
                payload = {
                    "id": 0,
                    "version": 0,
                    "firstName": partner.name,
                    "email": partner.email,
                    
                }
                print("::::::::::::::::::::payload::::::::::", payload)
                response = requests.post(url, headers=headers, json=payload)
                print("---------------response---------", response)

                if response.status_code == 200:
                    json_data = response.json()
                    self.process_tripletex_response(json_data)
                else:
                    print(f": {response.status_code}, {response.text}")

        except Exception as e:
            print(f"Error during request: {e}")

            
            
            
            
            
            
          




    def import_tripletex_product(self):
        print("::::::::::::::::::::PRODUCT IMPORT::::::::::::::::::::::::::")
        url = 'https://api.tripletex.io/v2/product'
        consumer_token = self.consumer_token 
        employee_token = self.employee_token
        company_id = '12841878'
        session_token = self.token

        auth_token = f'{company_id}:{session_token}'
        print("::::::::::::::::::::::::::::::::::AUTH TOKEN:::::::::::::::::::::::::::::::::::::", auth_token)
        encoded_token = base64.b64encode(auth_token.encode('utf-8')).decode('utf-8')
        print("::::::::::::::::::::::::::::::::::ENCODED TOKEN:::::::::::::::::::::::::::::::::::::", encoded_token)

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Basic {encoded_token}',
            'consumerToken': consumer_token,
            'employeeToken': employee_token
        }

        try:
            response = requests.get(url, headers=headers)
            print(":::::::::::::::::::::::::::::::::::::::::::RESPONSE:::::::::::::::::::::::::::::::::::::::::::::::::", response)

            if response.status_code == 200:
                json_data = response.json()
                print("::::::::::::::::::::::::::::::::::::::::::::::JSON::::::::::::::::::::::::::::::::::::::::::", json_data)
                self.process_tripletex_products(json_data['values'])

            else:
                print(f"Error: {response.status_code}, {response.text}")
                print("::::::::::::::::::::::::::::::::::::::::::::::ELSE RESPONSE::::::::::::::::::::::::::::::::::::::::::")


        except Exception as e:
            print(f"Error during request: {e}")
            
            
            
            
            

    @api.model
    def process_tripletex_products(self, tripletex_products):
        print("::::::::::::::::::::::::::::::::::::::::::::SECOND_TRIPLEX_PRODUCT_FUNCTION::::::::::::::::::::::::::::::::::::::::::::::::::")
        for product in tripletex_products:
            print("::::::::::::::::::::::::::::::::::::::::::::PRODUCT::::::::::::::::::::::::::::::::::::::::::::::::::",product)
            product_data = {
                'name': f"{product.get('name', '')}",
            }
            self.env['product.template'].create(product_data)
            print("::::::::::::::::::::::::::::::::::::::::::::PARTNER_DATA_CREATE::::::::::::::::::::::::::::::::::::::::::::::::::",product_data)

    
    def tripletex_import_taxes(self):
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
            