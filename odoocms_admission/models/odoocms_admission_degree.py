import pdb

from odoo import fields, models, _, api


class OdooCmsAdmissionDegree(models.Model):
    _name = 'odoocms.admission.degree'
    _description = 'Admission Education Degree'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    year_age = fields.Integer(string='Year of Education')
    admission_education_id = fields.Many2one('odoocms.admission.education')
    specialization_ids = fields.One2many('applicant.academic.group', 'degree_id')
