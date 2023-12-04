import base64
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import requests
import json
import logging

_logger = logging.getLogger(__name__)


class triplexAccount(models.Model):
    _inherit = 'account.account'

    triplex_account_id = fields.Char(string="Triplex Account Id")