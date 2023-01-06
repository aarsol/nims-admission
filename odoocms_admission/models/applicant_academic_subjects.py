from odoo import fields, models, _, api


class ApplicantAcademicSubects(models.Model):
    _name = 'applicant.academic.subjects'
    _description = 'Applicant Academic Subjects'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    academic_group_id = fields.Many2one('applicant.academic.group')
