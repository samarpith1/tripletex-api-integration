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

    #sale_order
    orderDateFrom = fields.Date(string="Order Date From:")
    orderDateTo = fields.Date(string="Order Date To:")
    from_count = fields.Char(string="From:")
    count = fields.Char(string="Count:")
    
    
    
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
            print(":::::::::::::::::::::::::::::::::::::::::::::NEW CUSTOMER DATA CREATION:::::::::::::::::::::::::::::::::::",contact)           
            partner_data = {
                'name': f"{contact.get('firstName', '')} {contact.get('lastName', '')}",
                'email': contact.get('email'),
                'mobile': str(contact.get('phoneNumberMobile', '')),
                'phone': contact.get('phoneNumberWork', ''),
                'tripletex_contact_id': contact.get('id'),                
            }
            print(":::::::::::::::::::::::::::::::::::::::::::::NEW CUSTOMER DATA PARTNER DATA:::::::::::::::::::::::::::::::::::",partner_data)


            
            partner = self.env['res.partner'].search([('tripletex_contact_id', '=', partner_data['tripletex_contact_id'])])
            print(":::::::::::::::::::::::::::::::::::::::::::::CHECKING CUSTOMER VALIDATIONS:::::::::::::::::::::::::::::::::::",partner)

            

            if partner:
                partner.write(partner_data)
                print(":::::::::::::::::::::::::::::::::::::::::::::WRITE CUSTOMER DETAILS:::::::::::::::::::::::::::::::::::",partner)

            else:                
                partner_id = self.env['res.partner'].create(partner_data)
                print(":::::::::::::::::::::::::::::::::::::::::::::<<<<<<<<CREATED NEW CUSTOMER WITH THE DETAILS>>>>>>>>>>:::::::::::::::::::::::::::::::::::",partner)

                


    
    
    
    
 

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
        try:
            products = self.env['product.template'].search([])

            for product in products:
                print("::::::::::::::::::::::::::::::::::::::::::::::::::PRODUCT::::::::::::::::::::::::::::::::::::::::::::::::::",product)
                url = 'https://api.tripletex.io/v2/product'
                consumer_token = self.consumer_token 
                employee_token = self.employee_token 
                print("::::::::::::::::::::::::::::::::::::::::::::::::::CONSUMER::::::::::::::::::::::::::::::::::::::::::::::::::",consumer_token)
                print("::::::::::::::::::::::::::::::::::::::::::::::::::EMPLOYEE::::::::::::::::::::::::::::::::::::::::::::::::::",employee_token)
                company_id = '12841878' 
                session_token = self.token  
                print("::::::::::::::::::::::::::::::::::::::::::::::::::SESSION::::::::::::::::::::::::::::::::::::::::::::::::::",session_token)


            
                auth_token = f'{company_id}:{session_token}'
                print("::::::::::::::::::::::::::::::::::::::::::::::::::AUTH TOKEN::::::::::::::::::::::::::::::::::::::::::::::::::",auth_token)

                encoded_token = base64.b64encode(auth_token.encode('utf-8')).decode('utf-8')
                print("::::::::::::::::::::::::::::::::::::::::::::::::::ENCODED TOKEN::::::::::::::::::::::::::::::::::::::::::::::::::",encoded_token)


                headers = {
                    'Accept': 'application/json',
                    'Authorization': f'Basic {encoded_token}',
                    'consumerToken': consumer_token,
                    'employeeToken': employee_token
                }
                print("::::::::::::::::::::::::::::::::::::::::::::::::::HEADERS::::::::::::::::::::::::::::::::::::::::::::::::::",headers)
                
                payload = {
                    "id": 0,
                    "version": 0,
                    "name": product.name,
                    "costExcludingVatCurrency": product.standard_price,
                    "priceIncludingVatCurrency": product.list_price,
                    
                }
                print(":::::::::::::::::::::::::::::::::::::::PAYLOAD:::::::::::::::::::::::::::::::::", payload)
                response = requests.post(url, headers=headers, json=payload)
                print("::::::::::::::::::::::::::::::::::::::::::::::RESPONSE::::::::::::::::::::::::::::::::::::::::::::::::::::", response)

        except Exception as e:
            print(f"Error during request: {e}")
           





            









    def tripletex_import_saleorder(self):
        print("::::::::::::::::::::PRODUCT IMPORT::::::::::::::::::::::::::")
        url = 'https://api.tripletex.io/v2/order'
        orderDateFrom = self.orderDateFrom
        orderDateTo = self.orderDateTo
        date1 = orderDateFrom.strftime('%Y-%m-%d')
        date2 = orderDateTo.strftime('%Y-%m-%d')
        from_count =  self.from_count
        count = self.count

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
        print(":::::::::::::::::::::::::::::::::::::::::::HEADERS:::::::::::::::::::::::::::::::::::::::::::::::::", headers)


        params = {
            'orderDateFrom': date1, 
            'orderDateTo': date2, 
            'from': from_count, 
            'count': count 
        }

        print(":::::::::::::::::::::::::::::::::::::::::::PARAMS:::::::::::::::::::::::::::::::::::::::::::::::::", params)
        
        


        try:
            response = requests.get(url, headers=headers, params=params)
            print(":::::::::::::::::::::::::::::::::::::::::::RESPONSE:::::::::::::::::::::::::::::::::::::::::::::::::", response.text)

            if response.status_code == 200:
                print(":::::::::::::::::::::::::::::::::::::::::::SUCCESS:::::::::::::::::::::::::::::::::::::::::::::::::")
                parsed_data = response.json()
                print("::::::::::::::::::::::::::::::::::::::::::::::JSON::::::::::::::::::::::::::::::::::::::::::", parsed_data)
                self.process_tripletex_import_saleorders(parsed_data['values'])

            else:
                print("::::::::::::::::::::::::::::::::::::::::::::::ELSE RESPONSE::::::::::::::::::::::::::::::::::::::::::")


        except Exception as e:
            print(f"Error during request: {e}")




    def get_sale_order_line(self,order_line):
        print(":::::::::::::::::order_line in GET SALE ORDER LINE Fn::::::::::::",order_line)
        url = "https://"+order_line
        print(":::::::::::::::;;:::::::::::::::::::::::::::::::::::::URL:::::::::::::::::::::::::",url)
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
        response = requests.get(url, headers=headers)
        print("::::::::::::::::::RESPONSE GET SALE ORDER LINE::::::::::::::::",response.text)




    @api.model
    def process_tripletex_import_saleorders(self, tripletex_saleorders):
        print("::::::::::::::::::::::::::::::::::::::::::::::SECOND FN::::::::::::::::::::::::::::::::::::::::::")

        for sale in tripletex_saleorders:
            print("::::::::::::::::::::::::::::::::::::::::::::::SALE::::::::::::::::::::::::::::::::::::::::::",sale)
            customer_id = sale.get("customer", {}).get("id")
            customer_detail_url = sale.get("customer",{}).get("url")
            
            order_lines = sale.get("orderLines", [])
            order_lines_urls = [order_line.get("url") for order_line in order_lines]
            
            print(":::::::::::::::::::::::::::::::::::::::::SALE ORDER LINE URLS::::::::::::::::::::::::::::::::::::",order_lines_urls)
            
            for order_line in order_lines_urls:                
                print("::::::::::::::::::::::::::::::::::ORDER LINE:::::::::::::::::::::::::::::::::::",order_line)                
                self.get_sale_order_line(order_line)

            print("::::::::::::::::::::::::::::::::::::::::::::::CUSTOMER URL::::::::::::::::::::::::::::::::::::::::::",customer_detail_url)
            print("::::::::::::::::::::::::::::::::::::::::::::::PRODUCT LINE URL::::::::::::::::::::::::::::::::::::::::::",product_line_url)

            self.env['res.partner']

            sale_order_data = {        
                # 'partner_id': sale.get('id'),            
                'date_order': sale.get('orderDate'),
                'tripletex_sale_order_id': sale.get('id'),                
            }
            print("::::::::::::::::::::::::::::::::::::::::::::::SALE_ORDER_DATA_DICT::::::::::::::::::::::::::::::::::::::::::",sale_order_data)


            partner_data = {
                'tripletex_contact_id' : customer_id,
                'name' : sale.get('customerName')
            }

            # order_line_data = {
            #     'product_template_id' : order_line.get('orderLines')
            # }
            # print("::::::::::::::::::::::::::::::::::::::::::::::ORDER_LINE_DATA::::::::::::::::::::::::::::::::::::::::::",order_line_data)


            print("::::::::::::::::::::::::::::::::::::::::::::::PARTNER_DATA_DICT::::::::::::::::::::::::::::::::::::::::::",partner_data)


            
            order = self.env['sale.order'].search([('tripletex_sale_order_id', '=', sale_order_data['tripletex_sale_order_id'])])
            print("::::::::::::::::::::::::::::::::::::::::::::::ORDER VALIDATION USING TRIPLETEX ID::::::::::::::::::::::::::::::::::::::::::",order)
            
            res_partner = self.env['res.partner'].sudo().search([('tripletex_contact_id', '=', customer_id)],limit=1)
            print("::::::::::::::::::::::::::::::::::::::::::::::RES PARTNER SEARCHING::::::::::::::::::::::::::::::::::::::::::",res_partner)


            if not res_partner:
                print("::::::::::::::::::::::::::::::::::NOT RES PARTNER:::::::::::::::::::::::::::::::::::")
                self.create_customer_from_sale_order(customer_detail_url)
                print("((((((((((((((((((((((((((((((((((((((((((((((((1))))))))))))))))))))))))))))))))))))))))))))))))")
                self.create_saleorderline_product(product_line_url)
                print("((((((((((((((((((((((((((((((((((((((((((((((((2))))))))))))))))))))))))))))))))))))))))))))))))")


                res_partner = self.env['res.partner'].sudo().search([('tripletex_contact_id', '=', customer_id)],limit=1)
                partner_id= res_partner.id
            else:
                partner_id = res_partner.id 
                print("::::::::::::::::::::::::::::::::::::::::::::::CREATED WRITE::::::::::::::::::::::::::::::::::::::::::",partner_id)

            sale_order_data['partner_id']=partner_id     
            if order:
                print("::::::::::::::::::::::::::::::::::::::::::::::WRITE::::::::::::::::::::::::::::::::::::::::::")
                order.write(sale_order_data)
            else: 
                create_order = self.env['sale.order'].create(sale_order_data)
                print("::::::::::::::::::::::::::::::::::::::::::::::CREATE::::::::::::::::::::::::::::::::::::::::::",create_order)


    def create_customer_from_sale_order(self,customer_detail_url):
        url = "https://"+customer_detail_url
        print(":::::::::::::::::::::::::::::::::::::::::::::CREATE URL::::::::::::::::::::::::::::::::::",url)
        consumer_token = self.consumer_token 
        employee_token = self.employee_token  
        company_id = '12841878' 
        session_token = self.token  

       
        auth_token = f'{company_id}:{session_token}'
        print(":::::::::::::::::::::::::::::::::::::::::::::AUTH TOKEN CUSTOMER::::::::::::::::::::::::::::::::::",auth_token)

        encoded_token = base64.b64encode(auth_token.encode('utf-8')).decode('utf-8')
        print(":::::::::::::::::::::::::::::::::::::::::::::ENCODED TOKEN CUSTOMER::::::::::::::::::::::::::::::::::",encoded_token)


        headers = {
            'Accept': 'application/json',
            'Authorization': f'Basic {encoded_token}',
            'consumerToken': consumer_token,
            'employeeToken': employee_token
        }
        print(":::::::::::::::::::::::::::::::::::::::::::::HEADERS CUSTOMER::::::::::::::::::::::::::::::::::",headers)


        try:
            print(":::::::::::::::::::::::::::::::::::::::::::::TRY CUSTOMER::::::::::::::::::::::::::::::::::")
            response = requests.get(url, headers=headers)
            print(":::::::::::::::::::::::::::::::::::::::::::::::CREATE SALE ORDER CUSTOMER RESPONSE::::::::::::::::::::::::::::::",response.text)

            if response.status_code == 200:
                print(":::::::::::::::::::::::::::::::::::::::::::::::response.status_code == 200::::::::::::::::::::::::::::::")  
                json_data = response.json()
                print(":::::::::::::::::::::::::::::::::::::::::::::::JSON DATA  OF CUSTOMER SALEORDER::::::::::::::::::::::::::::::",json_data)  
                # self.process_tripletex_sale_order_create_customer(json_data['value'])

            else:
                print(f"Error: {response.status_code}, {response.text}")

        except Exception as e:
            print(f"Error during request: {e}")
                





    def create_saleorderline_product(self,product_line_url):
        url = "https://"+product_line_url
        print(":::::::::::::::::::::::::::::::::::::::::::::CREATE PRODUCT LINE URL::::::::::::::::::::::::::::::::::",url)
        consumer_token = self.consumer_token 
        employee_token = self.employee_token  
        company_id = '12841878' 
        session_token = self.token  

       
        auth_token = f'{company_id}:{session_token}'
        print(":::::::::::::::::::::::::::::::::::::::::::::AUTH TOKEN SALE ORDER::::::::::::::::::::::::::::::::::",auth_token)

        encoded_token = base64.b64encode(auth_token.encode('utf-8')).decode('utf-8')
        print(":::::::::::::::::::::::::::::::::::::::::::::ENCODED TOKEN SALE ORDER::::::::::::::::::::::::::::::::::",encoded_token)


        headers = {
            'Accept': 'application/json',
            'Authorization': f'Basic {encoded_token}',
            'consumerToken': consumer_token,
            'employeeToken': employee_token
        }
        print(":::::::::::::::::::::::::::::::::::::::::::::HEADERS SALE ORDER::::::::::::::::::::::::::::::::::",headers)


        try:
            print(":::::::::::::::::::::::::::::::::::::::::::::TRY SALE ORDER LINE::::::::::::::::::::::::::::::::::")
            response = requests.get(url, headers=headers)
            print(":::::::::::::::::::::::::::::::::::::::::::::::CREATE SALE ORDER PRODUCT LINE RESPONSE::::::::::::::::::::::::::::::",response.text)

            if response.status_code == 200:
                print(":::::::::::::::::::::::::::::::::::::::::::::::response.status_code == 200 ::::::::::::::::::::::::::::::")  
                json_data = response.json()
                print(":::::::::::::::::::::::::::::::::::::::::::::::JSON DATA  OF SALE ORDER LINE SALEORDER::::::::::::::::::::::::::::::",json_data)  
                # self.process_tripletex_sale_order_create_customer(json_data['value'])

            else:
                print(f"Error: {response.status_code}, {response.text}")

        except Exception as e:
            print(f"Error during request: {e}")















 
        

 









































    























