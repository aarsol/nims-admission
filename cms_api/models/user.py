# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime, date

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    secret = fields.Char('Secret')
    
    
class OdooCMSAdmissionApplication(models.Model):
    _inherit = 'odoocms.application'

    tran_auth_id = fields.Char('Trans Auth')
    paid_amount = fields.Integer('Paid Amount')
    paid_date = fields.Char('Paid Date')
    paid_time = fields.Char('Paid Time')
    expiry = fields.Date('Expiry Date', compute='get_expiry_date',store=True)
    
    
    def get_expiry_date(self):
        return self.voucher_issued_date + relativedelta(days=7)
   