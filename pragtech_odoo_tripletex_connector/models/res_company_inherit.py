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
    
    #purchaseOrder
    deliveryDateFrom = fields.Date(string='Delivery Date From')
    deliveryDateTo = fields.Date(string='Delivery Date To')
    from_count = fields.Char(string='From Count')
    count = fields.Char(string='Count')
    
    
    
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
            

            partners = self.env['res.partner'].search([('tripletex_contact_id', '=', False)])

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
                if not partner.tripletex_contact_id:
                        response = requests.post(url, headers=headers, json=payload)
                        print("---------------response---------", response)
                        print(f": {response.status_code}, {response.text}")
               
                

                # if response.status_code == 200:
                #     json_data = response.json()
                #     self.process_tripletex_response(json_data)
                # else:
                #     print(f": {response.status_code}, {response.text}")

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

    
    
            
    def tripletex_import_chart_of_accounts(self):
        url = 'https://api.tripletex.io/v2/ledger/account'
        consumer_token = self.consumer_token 
        employee_token = self.employee_token  
        company_id = '12841878' 
        session_token = self.token  

   
        auth_token = f'{company_id}:{session_token}'
        encoded_token = base64.b64encode(auth_token.encode('utf-8')).decode('utf-8')
        print(":::::::::::encoded_token::::::::::", encoded_token)
        headers = {
        'Accept': 'application/json',
        'Authorization': f'Basic {encoded_token}',
        'consumerToken': consumer_token,
        'employeeToken': employee_token
         }
    
        try:
            response = requests.get(url, headers=headers)
            print(":::::::::::response:::::::", response)

            if response.status_code == 200:
                
                json_data = response.json()
                print(":::::::::::json_data",json_data)
                self.process_tripletex_chart_of_accounts(json_data['values'])

            else:
                print(f"Error: {response.status_code}, {response.text}")

        except Exception as e:
            print(f"Error during request: {e}")
            
        
    @api.model
    def process_tripletex_chart_of_accounts(self, tripletex_chart_of_accounts):
        for chart_of_account in tripletex_chart_of_accounts:
            account_type = 'asset_current'
        
            charter_data = {
                
                'name': f"{chart_of_account.get('name', '')}",
                'code': chart_of_account.get('number'),
                'account_type': account_type,
                # 'account_type': self.map_tripletex_account_type(chart_of_account.get('type')),
                # 'reconcile': chart_of_account.get('requireReconciliation', ''),
                 
                # 'currency_id': chart_of_account.get('currency',''),

                'tripletex_account_id': chart_of_account.get('id'),
                
            }
            print(":::::::::::::::::charter_data::::::::::::::",charter_data)
            
            

            
            charts = self.env['account.account'].search([('tripletex_account_id', '=', charter_data['tripletex_account_id'])])
            print(":::::::::::::::::charts::::::::::",charts)

            if charts:
                charts.write(charter_data)
                print("::::::::::::::::::::::::::::::::::::::charts:::::::::::::::::::::::::",charts)
            else:
                
                
                charter_id = self.env['account.account'].create(charter_data)
                print(":::::::::::::::::::::::::;charter_data:::::::::::",charter_data)

    
    def export_chart_of_accounts_to_tripletex(self):
        
        try:
            # charter_data1 = {
            #             'tripletex_account_id': chart_of_account.get('id')
            #             }
            chart_of_accounts = self.env['account.account'].search([('tripletex_account_id', '=', False)])
            for chart_of_account in chart_of_accounts:
               
                
                
            
           
               
       
                url = 'https://api.tripletex.io/v2/ledger/account'
                consumer_token = self.consumer_token 
                employee_token = self.employee_token  
                company_id = '12841878' 
                session_token = self.token  

            
                auth_token = f'{company_id}:{session_token}'
                print("::::::::::::::::::;authtoken::::",auth_token)
                encoded_token = base64.b64encode(auth_token.encode('utf-8')).decode('utf-8')
                print(":::::::::::::encoded_token::::",encoded_token)

                headers = {
                    'Accept': 'application/json',
                    'Authorization': f'Basic {encoded_token}',
                    'consumerToken': consumer_token,
                    'employeeToken': employee_token
                }
                print("::::::::::::::::headers::::::::",headers)
                
                payload = {
                    
                    # "id": chart_of_account.tripletex_account_id,
                    "version": 0,
                    "name": chart_of_account.name,
                    "number": chart_of_account.code,
                    
                    
                }
                print("::::::::::::::::::::payload::::::::::",payload)
                if not chart_of_account.tripletex_account_id:
                    response = requests.post(url, headers=headers, json=payload)
                    print(f": {response.status_code}, {response.text}")
                    if response.status_code == 201:
                        json_data = response.json()
                        print("::::::::::::::::sddsdfs",json_data)
                        chart_of_account.tripletex_account_id = json_data.get('value').get('id')
                        print("::::::::sdfdsdffgh:::::::::::",chart_of_account.tripletex_account_id)
                        
                        
                            
                        
                    else:
                        print(f": {response.status_code}, {response.text}")
                        
              


                    
      


                
        except Exception as e:
            print(f"Error during request: {e}")
            

    def tripletex_import_supplier(self):
            url = 'https://api.tripletex.io/v2/supplier'
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
                print("::::::::::::::::response::::::",response.text)

                if response.status_code == 200:
                    print(":::response::::::::::::::::::::::::::::::::::::::::::::::::::::",response)
                    
                    json_data = response.json()
                    self.process_tripletex_suppliers(json_data['values'])
                    # print("::::::::::::::::json_data:::::::",json_data)

                else:
                    print(f"Error: {response.status_code}, {response.text}")

            except Exception as e:
                print(f"Error during request: {e}")
                
                
            
            
            

    @api.model
    def process_tripletex_suppliers(self, tripletex_suppliers):
        print(":::::::::::tripletex_suppliers::::::::::::::::::::::::::::::::::::::",tripletex_suppliers)
        for tripletex_supplier in tripletex_suppliers:
            print("::::::::::::tripletex_supplier:::::::::::",tripletex_supplier)
            supplier_data = {
                'name': tripletex_supplier.get('name', ''),
                
                'email': tripletex_supplier.get('email'),
                'mobile': str(tripletex_supplier.get('phoneNumberMobile', '')),
                'phone': tripletex_supplier.get('phoneNumber', ''),
                'tripletex_supplier_id': tripletex_supplier.get('id'),
                
                
            }
            print("::::::::::::supplier_data:::::::::::::::::::::::::::::",supplier_data)

            
            suppliers = self.env['res.partner'].search([('tripletex_supplier_id', '=', supplier_data['tripletex_supplier_id'])])
            print(":::::::::suppliers:::::::::::::::::::::::::::::::::::",suppliers)

            if suppliers:
                suppliers.write(supplier_data)
                print(":::::::::writed suppliers:::::::::::::::::::::::::::::::::::::::::::::",suppliers)
                
            else:
                suppliers = self.env['res.partner'].create(supplier_data)
                
                
            
    def export_supplier_to_tripletex(self):
            
        try:
          
            suppliers = self.env['res.partner'].search([('tripletex_supplier_id', '=', False)])
            for supplier in suppliers:
               
                url = 'https://api.tripletex.io/v2/supplier'
                consumer_token = self.consumer_token 
                employee_token = self.employee_token  
                company_id = '12841878' 
                session_token = self.token  

            
                auth_token = f'{company_id}:{session_token}'
                print("::::::::::::::::::;authtoken::::",auth_token)
                encoded_token = base64.b64encode(auth_token.encode('utf-8')).decode('utf-8')
                print(":::::::::::::encoded_token::::",encoded_token)

                headers = {
                    'Accept': 'application/json',
                    'Authorization': f'Basic {encoded_token}',
                    'consumerToken': consumer_token,
                    'employeeToken': employee_token
                 }
                # print("::::::::::::::::headers::::::::",headers)
                
                payload = {
                    
                    # "id": chart_of_account.tripletex_account_id,
                    "version": 0,
                    "name": supplier.name,
                    "email": supplier.email,
                    "phoneNumberMobile":supplier.mobile,
                    "phoneNumber" :supplier.phone
                   
                    
                }
                # print("::::::::::::::::::::payload::::::::::",payload)
                if not supplier.tripletex_supplier_id:
                    response = requests.post(url, headers=headers, json=payload)
                    print(f": {response.status_code}, {response.text}")
                    print("response=======================",response.text)
                    if response.status_code == 201:
                        response_json = response.json()
                        print(":::::::::::::response_json::::::",response_json)
                        supplier.tripletex_supplier_id = response_json.get('value').get('id')
                        print(":::::::::::sdsdsdsdsd", response_json.get('value'), response_json.get('value').get('id'))
                        print("=======supplier.tripletex_supplier_id================",supplier.tripletex_supplier_id)

                else:
                     print("hello")
        
        except Exception as e:
                print(f"Error during request: {e}")
    
    
    

    def import_purchase_orders(self):
        url="https://api.tripletex.io/v2/purchaseOrder"
        deliveryDateFrom = self.deliveryDateFrom
        deliveryDateTo = self.deliveryDateTo
        from_count =  self.from_count
        count = self.count
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
        
        params = {
            'deliveryDateFrom': deliveryDateFrom, 
            'deliveryDateTo': deliveryDateTo, 
            'from': from_count, 
            'count': count 
        }

        
        
        try:
            response = requests.get(url, headers=headers, params=params)
           

            if response.status_code == 200:
               
                parsed_data = response.json()
                
                self.process_tripletex_import_purchaseorders(parsed_data['values'])
        
        except Exception as e:
            print(f"Error during request: {e}")

       
                    
                            
            
       
          
    def create_new_supplier(self,supplier_detail):
        
        
        url = "https://"+supplier_detail
        print(":::::::::::::::;;:::::::::::::::::::::::::::::::::::::url:::::::::::::::::::::::::",url)
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
                tripletex_supplier = json_data['value']
                supplier_data = {
                'name': tripletex_supplier.get('name', ''),
                'email': tripletex_supplier.get('email'),
                'mobile': str(tripletex_supplier.get('phoneNumberMobile', '')),
                'phone': tripletex_supplier.get('phoneNumber', ''),
                'tripletex_supplier_id': tripletex_supplier.get('id'),
                }
               
                
                suppliers = self.env['res.partner'].search([('tripletex_supplier_id', '=', supplier_data['tripletex_supplier_id'])])
                

                if suppliers:
                    suppliers.write(supplier_data)
                   
                    
                else:
                    suppliers = self.env['res.partner'].create(supplier_data)
                    
                return suppliers
        except Exception as e:
                print(f"Error during request: {e}")
                
    
    
            # if response.status_code == 200:
                
                
        #         json_data = response.json()
        #         print(":::::::::::::::::::::::::::json_data::::::::::::::::::::::::::::::::",json_data)
        #         tripletex_product = json_data['value']
        #         print(":::::::::::::::::::::::::::tripletex_product::::::::::::::::::::::::::::::::",tripletex_product)
        #         product_data = {
        #         'name': f"{tripletex_product.get('name', '')}",
        #         'product_qty': tripletex_product.get('number'),
        #         'description': str(tripletex_product.get('description', '')),
        #         'price_unit': tripletex_product.get('priceIncludingVatCurrency', ''),
        #         'tripletex_product_id': tripletex_product.get('id'),
        #         }
                
        #         products = self.env['purchase.order'].search([('tripletex_product_id', '=', product_data['tripletex_product_id'])])
        #     if products:
        #             products.write(product_data)
                   
                    
        #     else:
        #             products = self.env['purchase.order'].create(product_data)
                    
        #             return products  
            
        # except Exception as e:
        #         print(f"Error during request: {e}")
        
   
            
        
    def get_purchase_order_line(self,order_line):
        print(":::::::::::::::::order_line::::::::::::",order_line)
        url = "https://"+order_line
        print(":::::::::::::::;;:::::::::::::::::::::::::::::::::::::order_lines_str23422:::::::::::::::::::::::::",url)
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
            print("::::::::::::::::::response12222222222::::::::::::::::",response.text)
            json_data = response.json()
            print(":::::::::::::::::::::::::::json_data::::::::::::::::::::::::::::::::",json_data)
            tripletex_product = json_data['value']
            print(":::::::::::::::::::::::::::tripletex_product::::::::::::::::::::::::::::::::",tripletex_product)
           
            product_data = {
                'name': f"{tripletex_product.get('name', '')}",
                'product_qty': tripletex_product.get('number'),
                'description': str(tripletex_product.get('description', '')),
                
           }
            
            
            
        except Exception as e:
                print(f"Error during request: {e}")   
            
            
    
      
    @api.model
    def process_tripletex_import_purchaseorders(self, tripletex_purchaseorders):
        for purchase in tripletex_purchaseorders:
            print(":::::::::::::purchase::::::::::::",purchase)        
            supplier_id = purchase.get("supplier", {}).get("id")            
            supplier_detail = purchase.get("supplier",{}).get("url")           
            order_lines = purchase.get("orderLines", [])
            order_lines_urls = [order_line.get("url") for order_line in order_lines]            
            print(":::::::::::::::::order_lines_urls::::::::::::::::::::::::",order_lines_urls)            
            for order_line in order_lines_urls:                
                self.get_purchase_order_line(order_line)
            
            
            
            
            
            
            
            
            # for order_line_data in order_lines_ids:
            #     order_detail = order_line_data.get("url")
            
            
            
            # partner = self.create_new_supplier(supplier_detail)
            # product = self.create_new_product(order_lines_str)
                
            

            # purchase_order_data = {        
            #     'partner_id': partner.id,          
            #     'date_order': purchase.get('deliveryDate'),
            #     'tripletex_purchase_order_id': purchase.get('id')              
            # }
            
            # purchase_order_lines = {
            #     'product_id': product.id,
            #     'name': product.get('name'),
            #     'product_qty':product.get('quantityReceived'),
            #     'price_unit': product.get('priceIncludingVatCurrency'),
            #     'price_subtotal': product.get('amountIncludingVatCurrency')
                
            # }
            
        
            
            # purchase_orders = self.env['purchase.order'].search([('tripletex_purchase_order_id', '=', purchase_order_data['tripletex_purchase_order_id'])])
            # purchase_order_lines = self.env['purchase.order.line'].search([('product_id','=',purchase_order_lines['product_id'])])
            
            #if purchase_orders and purchase_order_lines:
            
            #     # purchase_orders.write(purchase_order_data)
            # else: 
            #     create_purchase_order = self.env['purchase.order'].create(purchase_order_data)
                