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
    expiry_date = fields.Date('Expiry Date', compute='_get_expiry_date',store=True)
    
    @api.depends('voucher_issued_date')
    def _get_expiry_date(self):
        for rec in self:
            if rec.voucher_issued_date:
                rec.expiry_date =  rec.voucher_issued_date + relativedelta(days=7)
   