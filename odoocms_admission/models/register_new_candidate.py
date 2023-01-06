import pdb

from odoo import fields, models, _, api
import random
import string
import logging
from datetime import datetime, date

from odoo.exceptions import UserError


class RegisterCandidate(models.Model):
    _name = 'register.candidate'
    _description = 'Register New Candidate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'first_name'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    email = fields.Char(string='Email', required=True)
    phone = fields.Char(string='Phone', size=11)
    fee_receipt_no = fields.Char(string='Fee Receipt No')
    amount = fields.Integer(string='Amount')
    cnic = fields.Char(string="CNIC", size=15)

    def sign_up(self):
        application = self.env['odoocms.application'].search([('email', '=', self.email)])
        length = 8
        all = string.ascii_letters + string.digits + '$#'
        password = "".join(random.sample(all, length))

        for rec in self:
            if rec.email != application.email:
                values = {
                    'first_name': rec.first_name,
                    'last_name': rec.last_name,
                    'email': rec.email,
                    'mobile': rec.phone,
                    'cnic': rec.cnic,
                    'fee_voucher_state': 'verify',
                    'voucher_date': fields.Date.today(),
                    'step_no': 1,
                }
                app_id = self.env['odoocms.application'].create(values)
                user_create = self.env['res.users'].sudo().create({
                    'name': str(rec.first_name) + ' ' + str(rec.last_name),
                    'sel_groups_1_9_10': 9,
                    'email': rec.email,
                    'user_type': 'student',
                    'login': app_id.application_no,
                    'phone': rec.phone,
                    'password': password,
                })
                app_id.user_id = user_create.id
                if user_create:
                    app_id.action_create_prospectus_invoice()
                    app_id.voucher_number = app_id.prospectus_inv_id and app_id.prospectus_inv_id.barcode or ''
                    app_id.amount = app_id.prospectus_inv_id.amount_total
                    rec.fee_receipt_no = app_id.voucher_number
                    rec.amount = app_id.amount
                    user = self.env['res.users'].sudo().search([('login', '=', app_id.application_no)])
                    template = self.env.ref('odoocms_admission.mail_template_account_created')
                    pass_val = {
                        'email':rec.email,
                        'password': password,
                        'login': app_id.application_no,
                        'company_name': self.env.company.name,
                        'company_website': self.env.company.website,
                        'company_email': self.env.company.admission_mail,
                        'company_phone': self.env.company.admission_phone,
                    }
                    template.with_context(pass_val).send_mail(user.id, force_send=True)
                    message_id = self.env['success.message.wizard'].create(
                        {'message': 'New Student Registered Successfully...'})
                    return {
                        'name': 'Message',
                        'type': 'ir.actions.act_window',
                        'view_mode': 'form',
                        'res_model': 'success.message.wizard',
                        'res_id': message_id.id,
                        'target': 'new'
                    }

            elif application.email == rec.email:
                raise UserError(_('Student Already Registered with this email.'))
