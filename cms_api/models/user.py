# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'
    
    secret = fields.Char('Secret')
    
    
class InheritMove(models.Model):
    _inherit = 'account.move'

    tran_auth_id = fields.Char('Trans Auth')
    paid_amount = fields.Integer('Paid Amount')
    paid_date = fields.Char('Paid Date')
    paid_time = fields.Char('Paid Time')
   