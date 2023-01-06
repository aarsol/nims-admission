

from odoo import fields, models, _, api


class PGCInstitute(models.Model):
    _name = 'pgc.institute'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'PGC Institute'

    name = fields.Char()


class PgcScholarship(models.Model):
    _name = 'applicant.pgc.scholarship'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Need Base Scholarship'
    _rec_name = 'previous_school_attend'

    previous_school_attend = fields.Char(string='Previous Institute Attend')
    pgc_registration_no = fields.Char(string='Previous Registration No')
    pgc_institute_id = fields.Many2one('pgc.institute', string='PGC Institute')
    # application_id = fields.Many2one('odoocms.application')
