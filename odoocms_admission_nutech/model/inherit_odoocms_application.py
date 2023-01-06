import pdb
from datetime import date
import random
import string

from odoo import fields, models, _, api


class OdooCMSInherit(models.Model):
    _inherit = 'account.move'
    _description = 'Account Move Admission Inherit'

    application_id = fields.Many2one('odoocms.application', string='Applicant')
    is_prospectus_fee = fields.Boolean(string='Is prospectus fee')

class OdooCMSInherit(models.Model):
    _inherit = 'odoocms.application'
    _description = 'Odoo CMS Inherit'

    # Need Base Scholarship
    guardian_occupation = fields.Char(string='Father/Guardian Occupation')
    guardian_job_status = fields.Selection(
        string='Guardian Job Status',
        selection=[('serving', 'Serving'),
                   ('retired', 'Retired'), ],
        required=False, default='serving')
    guardian_monthly_income = fields.Char(string='Father/Guardians Monthly Income')
    residential_status = fields.Selection(
        string='Residential Status',
        selection=[('r', 'Resident'),
                   ('nr', 'Non Resident'), ],
        required=False, default='r')
    family_member = fields.Char(string='Family Member')
    previous_school_attend = fields.Char(string='Previous Institute Attend')
    pgc_registration_no = fields.Char(string='Previous Registration No')
    pgc_institute_id = fields.Many2one('pgc.institute', string='PGC Institute')
    last_school_attend = fields.Many2one('last.institute.attend', string='Last Institute Attend'
                                         )
    cnic_front = fields.Binary('Cnic Front', attachment=True)
    cnic_back = fields.Binary('Cnic Back', attachment=True)
    domicile = fields.Binary('Domicile', attachment=True)
    pass_port = fields.Binary('Passport', attachment=True)
    invoice_visibility = fields.Boolean('Invoice Visibility')
    first_in_family = fields.Selection(string='Are you first in your family applying for university degree?',
                                        selection = [('no', 'No'),
                                                     ('yes', 'Yes'), ])
    first_in_family_detail = fields.Text(string='Family Study Detail')

    disabled_person = fields.Selection(string='Are you special person?',
                                       selection=[('no', 'No'),
                                                  ('yes', 'Yes'), ])

    disabled_person_detail = fields.Text(string='Disability Details')
    disease = fields.Selection(string='Do you have any chronical disease?',
                                       selection=[('no', 'No'),
                                                  ('yes', 'Yes'), ])
    disease_details = fields.Text(string='Disease Detail')
    password = fields.Char(string='Password')
    sat_score = fields.Float(string='SAT Score')
    education_consent = fields.Boolean(string='Education Consent')



    @api.onchange('fee_voucher_state')
    def assign_test_date(self):
        length = 8
        all = string.ascii_letters + string.digits + '$#'
        password = "".join(random.sample(all, length))

        for rec in self:
            program_check = self.env['odoocms.program'].search([])
            for check_program in program_check:
                if rec.fee_voucher_state == 'verify':
                    centers = self.env['odoocms.entry.test.schedule'].search([])
                    for center in centers:
                        for program in center.entry_test_schedule_ids:
                            if rec.preference_ids[
                                0].program_id.id == program.program_id.id and program.status == 'open':
                                if rec.preference_ids[0].program_id.id == check_program.id:
                                    if check_program.offering == True and check_program.entry_test == True and check_program.interview == True:
                                        applicant = self.env['applicant.entry.test'].sudo().create({
                                            'student_id': rec._origin.id,
                                            'entry_test_schedule_details_id': program.id,
                                            'cbt_password': password,
                                        })
                                        template = self.env.ref('odoocms_admission.mail_template_voucher_verified')
                                        post_message = rec.message_post_with_template(template.id,
                                                                                      composition_mode='comment')  # , composition_mode='comment'
                                        if applicant:
                                            template = self.env.ref('odoocms_admission_nutech.mail_template_test_email')
                                            template.with_context().send_mail(applicant.id, force_send=True)

                                        if program.capacity == program.count:
                                            program.status = 'full'

    def verify_voucher(self):
        length = 8
        all = string.ascii_letters + string.digits + '$#'
        password = "".join(random.sample(all, length))

        for rec in self:
            if rec.fee_voucher_state == 'upload':
                data = {
                    'fee_voucher_state': 'verify',
                    'voucher_date': date.today(),
                }
                rec.sudo().write(data)
                if rec.fee_voucher_state == 'verify':
                    program_check = self.env['odoocms.program'].search([])
                    for check_program in program_check:
                        centers = self.env['odoocms.entry.test.schedule'].search([])
                        for center in centers:
                            for program in center.entry_test_schedule_ids:
                                if rec.preference_ids[
                                    0].program_id.id == program.program_id.id and program.status == 'open':
                                    if rec.preference_ids[0].program_id.id == check_program.id:
                                        if check_program.offering == True and check_program.entry_test == True and check_program.interview == True:
                                            applicant = self.env['applicant.entry.test'].create({
                                                'student_id': rec.id,
                                                'entry_test_schedule_details_id': program.id,
                                                'cbt_password': password,
                                            })
                                            template = self.env.ref('odoocms_admission.mail_template_voucher_verified')
                                            post_message = rec.message_post_with_template(template.id,
                                                                                          composition_mode='comment')
                                            if applicant:
                                                template = self.env.ref(
                                                    'odoocms_admission_nutech.mail_template_test_email')
                                                template.with_context().send_mail(applicant.id, force_send=True)

                                                if program.capacity == program.count:
                                                    program.status = 'full'

        res = super(OdooCMSInherit, self).verify_voucher()
        return res


class OdooCMSProgramInherit(models.Model):
    _inherit = 'odoocms.program'
    _description = 'Odoo CMS Program Inherit'

    offering = fields.Boolean(string='Offering', default=True)
    payment = fields.Selection(
        string='Payment',
        selection=[('online', 'Online'),
                   ('voucher', 'Through Voucher'), ],
        required=False, )
    entry_test = fields.Boolean(string='Entry Test')
    interview = fields.Boolean(string='Interview')
    offer_letter = fields.Boolean(string='Offer Letter')
    date = fields.Date(string='Classes Start Date')
    description = fields.Html(string='Offer Letter Set Up')
    test_admit_card = fields.Html()
    interview_card_setup = fields.Html()


class OdooCmsRegisterInherit(models.Model):
    _inherit = 'odoocms.admission.register'
    _description = 'Odoo CMS Register Inherit'

    prospectus_fee_due_date = fields.Date(string='Registration Fee Due Date')
