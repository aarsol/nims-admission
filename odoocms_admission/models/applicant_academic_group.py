from odoo import fields, models, _, api


class AdmissionDocuments(models.Model):
    _name = 'applicant.academic.group'
    _description = 'Applicant Academic Group'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    degree_id = fields.Many2one('odoocms.admission.degree')
    academic_subject_ids = fields.One2many('applicant.academic.subjects', 'academic_group_id')
