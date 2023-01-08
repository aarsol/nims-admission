from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning
import pdb


class OdooCMSAdmissionRegister(models.Model):
    _name = "odoocms.admission.register"
    _description = "Admission Register"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Name', required=True, readonly=True, states={'draft': [('readonly', False)]})
    academic_session_id = fields.Many2one('odoocms.academic.session', 'Academic Session', required=True)
    term_id = fields.Many2one('odoocms.academic.term', 'Academic Term', required=False)
    career_id = fields.Many2one('odoocms.career', 'Career', required=True)
    date_start = fields.Date('Start Date', readonly=True, default=fields.Date.today(),
                             states={'draft': [('readonly', False)]})
    date_end = fields.Date('End Date', readonly=True, default=(fields.Date.today() + relativedelta(days=30)),
                           tracking=True, states={'draft': [('readonly', False)]})
    dob_min = fields.Date(string='DOB Minimum')
    dob_max = fields.Date(string='DOB Maximum')
    preferences_allowed = fields.Integer(string='Preferences Allowed')

    eligibility_criteria_image = fields.Binary('Eligibility criteria Image', states={'draft': [('readonly', False)]})
    program_ids = fields.Many2many('odoocms.program', 'register_program_rel', 'register_id', 'program_id',
                                   'Offered Programs')
    min_edu_year = fields.Integer(string='Minimum Education Year', default=12,required=True, )

    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirmed'),
         ('cancel', 'Cancelled'), ('application', 'Application Gathering'), ('sort', 'Application Stoped'),
         ('admission', 'Merit Process'), ('merit', 'Merit'), ('done', 'Done')],
        'Status', default='draft', tracking=True)

    application_ids = fields.One2many('odoocms.application', 'register_id', 'Admissions')

    # Test Series
    undertaking = fields.Html(string='Undertaking')
    # test_series_ids = fields.One2many('odoocms.admission.test.series', 'register_id', 'Test Series')

    def sort_applications(self):
        i = 1
        for application in self.application_ids.filtered(lambda l: l.state in ('approve', 'open', 'submit')).sorted(
                key=lambda r: r.merit_score, reverse=True):
            # for application in self.application_ids.filtered(lambda l: l.state in ('approve', 'open', 'submit')).sorted(key=lambda r: r.manual_score, reverse=True):

            if not application.preference_ids:
                raise UserError(
                    'Program Preference not set for %s - %s not Set.' % (
                        application.entry_registration, application.name))

            # if self.information_gathering:
            #     application.write({
            #         'program_id': application.preference_ids and application.preference_ids[0].program_id.id,
            #         'locked': True,
            #         'state': 'open',
            #         'preference': 1,
            #     })

            if application.cnic and len(application.cnic) == 13:
                application.cnic = application.cnic[:5] + '-' + application.cnic[5:12] + '-' + application.cnic[12:]

            application.merit_number = i
            i += 1

    @api.constrains('dob_max', 'dob_min')
    def date_constrains(self):
        for rec in self:
            if rec.dob_max > rec.dob_min:
                raise ValidationError(_('Sorry, DOB Max Date Must be Less Than DOB Min Date...'))

    @api.constrains('date_start', 'date_end')
    def check_dates(self):
        for record in self:
            start_date = fields.Date.from_string(record.date_start)
            end_date = fields.Date.from_string(record.date_end)
            if start_date > end_date:
                raise ValidationError(
                    _("End Date cannot be set before Start Date."))

    def confirm_register(self):
        self.state = 'confirm'

    def set_to_draft(self):
        self.state = 'draft'

    def cancel_register(self):
        self.state = 'cancel'

    def start_application(self):
        self.state = 'application'

    def stop_application(self):
        self.state = 'sort'

    def start_admission(self):
        self.sort_applications()
        self.state = 'admission'


class OdooCMSAdmissionMerit(models.Model):
    _name = "odoocms.admission.merit.criteria"
    _description = "Admission Merit Criteria"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    register_id = fields.Many2one('odoocms.admission.register', 'Admission Register', required=True)
    program_ids = fields.Many2many('odoocms.program', string='Program', required=True)
    matric_percentage = fields.Float('Matric Percentage', default=60,
                                     help='If this is not eligible for any program, Add percentage > 100')


class ResCompany(models.Model):
    _inherit = 'res.company'

    admission_phone = fields.Char()
