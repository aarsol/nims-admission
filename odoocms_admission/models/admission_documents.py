from odoo import fields, models, _, api


class AdmissionDocuments(models.Model):
    _name = 'applicant.academic.detail'
    _description = 'Applicant Document Details'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'application_id'

    application_id = fields.Many2one('odoocms.application', string='Applicant', ondelete='cascade')
    applicant = fields.Char(related='application_id.name', string='Applicant Name', store=True)
    program_id = fields.Many2one('odoocms.program', string='Program', compute="get_program", store=True)
    reference_no = fields.Char(related='application_id.application_no', string='Reference No', store=True)
    cnic = fields.Char(string='CNIC', related='application_id.cnic')
    cnic_attachment = fields.Binary(string='CNIC Attachment', related='application_id.cnic_front')
    board = fields.Char(string='Board')

    institute = fields.Char(string='Institute')
    passport = fields.Char(string='Passport', related='application_id.passport')
    passport_attachment = fields.Binary(string='Passport Attachment', related='application_id.pass_port')
    mobile = fields.Char(string='Mobile', related='application_id.mobile')
    gender = fields.Selection(
        string='Gender',
        selection=[('m', 'Male'),
                   ('f', 'Female'),
                   ('o', 'Other'), ],
        required=False, related='application_id.gender')
    domicile = fields.Char(string='Domicile', related='application_id.domicile_id.name')
    domicile_attachment = fields.Binary(string='Domicile Attachment', related='application_id.domicile')
    nationality = fields.Char(string='Nationality', related='application_id.nationality.name')
    doc_state = fields.Selection(
        [('yes', 'Verified'), ('no', 'UnVerified'), ('rejected', 'Rejected'),
         ('reg_verified', 'Registration Verified'), ('reg_reject', 'Registration Reject')],
        string='Verified?', default="no")
    doc_verify = fields.Boolean(default=False)
    reg_verify = fields.Boolean(default=False)
    degree_name = fields.Many2one('odoocms.admission.degree')
    degree_level_id = fields.Many2one('odoocms.admission.education')
    group_specialization = fields.Many2one('applicant.academic.group')
    application_id = fields.Many2one('odoocms.application')
    applicant_subject_id = fields.One2many('applicant.subject.details', 'applicant_academic_id')
    roll_no = fields.Char(string='Roll No')
    sec_year_roll_no = fields.Char(string='Second Year Roll No')
    result_status = fields.Selection(
        string='Result Status',
        selection=[('complete', 'Complete'),
                   ('waiting', 'Waiting'), ],
        required=False, )

    obt_marks = fields.Integer('Obtained Marks')
    total_marks = fields.Integer('Total Marks')
    obtained_cgpa = fields.Float('Obtained CGPA')
    total_cgpa = fields.Float('Total CGPA')
    
    percentage = fields.Float('Percentage')
    attachment = fields.Binary(string='Degree Attachment View', attachment=True)
    degree_attachment = fields.Binary('Degree Attachment Download', related='attachment')
    year = fields.Char(string='Passing Year')
    hope_certificate = fields.Image('Hope Certificate View', attachment=True)
    hope_certificate_attachment = fields.Image('Hope Certificate Download', related='hope_certificate')

    def action_document_verified(self):
        self.doc_verify = True
        for rec in self:
            rec.doc_state = 'yes'

    def action_document_unverified(self):
        self.doc_verify = True
        for rec in self:
            rec.doc_state = 'no'

    def registration_verified(self):
        self.reg_verify = True
        for rec in self:
            rec.doc_state = 'reg_verified'

    def registration_unverified(self):
        self.reg_verify = True
        for rec in self:
            rec.doc_state = 'reg_reject'

    def action_document_rejected(self):
        self.doc_verify = True
        for rec in self:
            rec.doc_state = 'rejected'

    def get_program(self):
        for rec in self:
            if len(rec.application_id.preference_ids)>0:
                rec.program_id = rec.application_id.preference_ids[0].program_id
