from odoo import _, models, fields,api
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
        consumer_token = self.consumer_token  # Replace with your consumer token
        employee_token = self.employee_token  # Replace with your employee token
        company_id = '12841878'  # Replace with your company ID
        session_token = self.token  # Replace with your session token

        # Create the authentication token
        auth_token = f'{company_id}:{session_token}'
        encoded_token = base64.b64encode(auth_token.encode('utf-8')).decode('utf-8')
        print("-----encoded:::::::::::::::::::::::::::::::::::::", encoded_token)

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Basic {encoded_token}',
            'consumerToken': consumer_token,
            'employeeToken': employee_token
        }

        try:
            response = requests.get(url, headers=headers)
            print("--------------response----------------------------", response)

            if response.status_code == 200:
                # Request was successful
                json_data = response.json()
                print("======================================JSON==============================", json_data)
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
                
            }

            partner = self.env['res.partner'].search([('email', '=', partner_data['email'])])

            if partner:
                partner.write(partner_data)
                print("----------------dfghjkjhgfdsa",partner_data)
            else:
               
                self.env['res.partner'].create(partner_data)
                print("-----partner",partner_data)



    
    def tripletex_export_contacts(self):
        print("-----work this print")




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
                'tripletex_product_id': product.get('id'),
                'list_price': product.get('priceIncludingVatCurrency'),
                'standard_price': product.get('costExcludingVatCurrency'),
                'weight': product.get('weight'),
                'weight_uom_name': product.get('weightUnit'),
                'volume': product.get('volume'),
                'volume_uom_name': product.get('volumeUnit'),
                
            }
            product_search = self.env['product.template'].search([('tripletex_product_id', '=', product_data['tripletex_product_id'])])
            # product_vendor_search = self.env['product.supplierinfo'].search([('partner_id', '=' product_data['partner_id'])])

            if product_search:
                product_search.write(product_data)
                print("::::::::::::::::::::::::::::::::::::::::::::PRODUCT_DATA_WRITE::::::::::::::::::::::::::::::::::::::::::::::::::",product_data)
            # if product_vendor_search:
            #     product_vendor_search.write(product_data)
            #     print("::::::::::::::::::::::::::::::::::::::::::::PRODUCT_VENDOR_WRITE::::::::::::::::::::::::::::::::::::::::::::::::::",product_data)
            else:
                self.env['product.template'].create(product_data)
                print("::::::::::::::::::::::::::::::::::::::::::::PRODUCT_DATA_CREATE::::::::::::::::::::::::::::::::::::::::::::::::::",product_data)
                # self.env['product.supplierinfo'].create(product_data)
                # print("::::::::::::::::::::::::::::::::::::::::::::PRODUCT_DATA_CREATE::::::::::::::::::::::::::::::::::::::::::::::::::",product_data)
                    









    def tripletex_export_products_main(self):
        print("::::::::::::::::::::PRODUCT EXPORT::::::::::::::::::::::::::")
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
            # response = requests.post(url, headers=headers)
            response = requests.request('POST', url=url, data=parsed_dict, headers=headers)

            print(":::::::::::::::::::::::::::::::::::::::::::RESPONSE:::::::::::::::::::::::::::::::::::::::::::::::::", response)

            if response.status_code == 200:
                json_data = response.json()
                print("::::::::::::::::::::::::::::::::::::::::::::::JSON::::::::::::::::::::::::::::::::::::::::::", json_data)
                self.process_export_tripletex_products(json_data['values'])

            else:
                print(f"Error: {response.status_code}, {response.text}")
                print("::::::::::::::::::::::::::::::::::::::::::::::ELSE RESPONSE::::::::::::::::::::::::::::::::::::::::::")


        except Exception as e:
            print(f"Error during request: {e}")
            
            
            
                

    @api.model
    def process_export_tripletex_products(self, tripletex_products):
        print("::::::::::::::::::::::::::::::::::::::::::::SECOND_TRIPLEX_PRODUCT_FUNCTION::::::::::::::::::::::::::::::::::::::::::::::::::")
        for product in tripletex_products:
            print("::::::::::::::::::::::::::::::::::::::::::::PRODUCT::::::::::::::::::::::::::::::::::::::::::::::::::",product)
            product_data = {
                'name': f"{product.post('name', '')}",
                # 'tripletex_product_id': product.get('id'),
                # 'list_price': product.get('priceIncludingVatCurrency'),
                # 'standard_price': product.get('costExcludingVatCurrency'),
                # 'weight': product.get('weight'),
                # 'weight_uom_name': product.get('weightUnit'),
                # 'volume': product.get('volume'),
                # 'volume_uom_name': product.get('volumeUnit'),
                
            }
            print("::::::::::::::::::::::::::::::::::::::::::::PRODUCT::::::::::::::::::::::::::::::::::::::::::::::::::",product_data)

            # product_search = self.env['product.template'].search([('tripletex_product_id', '=', product_data['tripletex_product_id'])])
            # product_vendor_search = self.env['product.supplierinfo'].search([('partner_id', '=' product_data['partner_id'])])

            # if product_search:
                # product_search.write(product_data)
                # print("::::::::::::::::::::::::::::::::::::::::::::PRODUCT_DATA_WRITE::::::::::::::::::::::::::::::::::::::::::::::::::",product_data)
            # if product_vendor_search:
            #     product_vendor_search.write(product_data)
            #     print("::::::::::::::::::::::::::::::::::::::::::::PRODUCT_VENDOR_WRITE::::::::::::::::::::::::::::::::::::::::::::::::::",product_data)
            # else:
                # self.env['product.template'].create(product_data)
                # print("::::::::::::::::::::::::::::::::::::::::::::PRODUCT_DATA_CREATE::::::::::::::::::::::::::::::::::::::::::::::::::",product_data)
                # self.env['product.supplierinfo'].create(product_data)
                # print("::::::::::::::::::::::::::::::::::::::::::::PRODUCT_DATA_CREATE::::::::::::::::::::::::::::::::::::::::::::::::::",product_data)
                    


    






















    # # @api.model
    # def tripletex_export_products_main(self):
    #     product_search = self.env['product.template'].search([])
    #     print("::::::::::::::::::::::::::::::::::PRODUCT SEARCH:::::::::::::::::::::::::::::::::::::::::::::::::",product_search)

    #     for products in product_search:
    #         print("::::::::::::::::::::::::::::::::::SUB FUNCTION:::::::::::::::::::::::::::::::::::::::::::::::::")
    #         self.triplex_export_product_sub(products)
        
        
    # def triplex_export_product_sub(self, products):
    #     url = 'https://tripletex.no/v2/contact'
        
    #     consumer_token = self.consumer_token
    #     print(":::::::::::::::::::::::::::::::::CONSUMER TOKEN::::::::::::::::::::::::::::::::::::::::::",consumer_token)
    #     employee_token = self.employee_token
    #     print("::::::::::::::::::::::::::::::::::::::::::::EMPLOYEE TOKEN:::::::::::::::::::::::::::::::::::::::::::::::::::",employee_token)
    #     tripletex_token = self.token
    #     print("::::::::::::::::::::::::::::::::::::::::::::::::TRIPLETEX TOKEN:::::::::::::::::::::::::::::::::::::::::;",tripletex_token)
    #     company_id = '98765'
        
    #     auth_token = f'{company_id}:{tripletex_token}'
    #     print(":::::::::::::::::::::::::::::::::::::::::::::::AUTH TOKEN:::::::::::::::::::::::::::::::::::::::::::::::::::",auth_token)
    #     encoded_token = base64.b64encode(auth_token.encode('utf-8')).decode('utf-8')
    #     print("::::::::::::::::::::::::::::::::::::::::::::::::::ENCODED TOKEN:::::::::::::::::::::::::::::::::::::::::::::::::::::::",encoded_token)

    #     headers = {
    #         'Accept': 'application/json',
    #         'Authorization': f'Tripletex {encoded_token}',
    #         'Content-Type': 'application/json; charset=utf-8',
    #         'consumerToken': consumer_token,
    #         'employeeToken': employee_token
    #     }
    #     print("::::::::::::::::::::::::::::::::::::::::::::::::::::HEADERS:::::::::::::::::::::::::::::::::::::::::::::::::::::::",headers)

    #     # Create the payload based on your Tripletex contact structure
    #     payload = {
    #         "id": 0,
    #         "version": 0,
    #         "name": products.name,
            
    #     }
    #     print(":::::::::::::::::::::::::::::::::::::::::::::::::::::PAYLOAD:::::::::::::::::::::::::::::::::::::::::::::::::::::::",payload)


    #     try:
    #         response = requests.post(url, headers=headers, json=payload)
    #         print("::::::::::::::::::::::::::::::::::::::::::::::::::RESPONSE::::::::::::::::::::::::::::::::::::::::::::::::::::::",response)

    #         if response.status_code == 200:
    #             json_data = response.json()
    #             print("::::::::::::::::::::::::::::::::::::::::::::::::::JSON DATA::::::::::::::::::::::::::::::::::::::::::::::::::::::",json_data)
    #             self.process_tripletex_response(json_data)  
    #         else:
    #             print("::::::::::::::::::::::::::::::::::::::::::::::::::JSON DATA ELSE PART::::::::::::::::::::::::::::::::::::::::::::::::::::::")
    #             print(f"Error: {response.status_code}, {response.text}")

    #     except Exception as e:
    #         print(f"Error during request: {e}")

    # def process_tripletex_response(self, response):
    #     print(":::::::::::::::::::::::::^^^^^^^^^<^>::::process_tripletex_response:::::::::::::::^^^^^^^^^^^^^^^^^^^::::::::::::::::::")


















#############################################from xero # #########################



    # @api.model
    # def create_main_customer_in_xero(self, con, xero_config):
    #     if con:
    #         vals = con.prepare_customer_export_dict()
    #         parsed_dict = json.dumps(vals)
    #         token = ''
    #         if xero_config.xero_oauth_token:
    #             token = xero_config.xero_oauth_token

    #         if not token:
    #             raise ValidationError('Token not found,Authentication Unsuccessful Please check your connection!!')

    #         headers = self.get_head()

    #         if token:
    #             protected_url = 'https://api.xero.com/api.xro/2.0/Contacts'
    #             data = requests.request('POST', url=protected_url, data=parsed_dict, headers=headers)
    #             if data.status_code == 200:
    #                 response_data = json.loads(data.text)
    #                 if response_data.get('Contacts'):
    #                     con.xero_cust_id = response_data.get('Contacts')[0].get('ContactID')
    #                     _logger.info("\nExported Contact : {} {}".format(con, con.name))
    #                     child_ids_all = self.search(
    #                         [('parent_id', '=', con.id), ('company_id', '=', xero_config.id)])
    #                     if child_ids_all:
    #                         for child in child_ids_all:
    #                             child.xero_cust_id = ''

    #                     child_ids = self.search([('parent_id', '=', con.id), ('company_id', '=', xero_config.id)],
    #                                             limit=5)
    #                     if child_ids:
    #                         for child in child_ids:
    #                             child.xero_cust_id = response_data.get('Contacts')[0].get('ContactID')
    #                             _logger.info("\nExported Sub-Contact : {} {}".format(child, child.name))