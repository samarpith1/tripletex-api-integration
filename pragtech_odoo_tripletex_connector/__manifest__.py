# -*- coding: utf-8 -*-
{
    'name': "pragtech_odoo_tripletex_connector",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','mail','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/session_token_create.xml',
        'views/res_company_inherit_view.xml',
        'views/session_token_view.xml',
        'views/menu.xml',
        'views/res_partner_inherit_view.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

