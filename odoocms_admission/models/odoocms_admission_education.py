import pdb

from odoo import fields, models, _, api


class OdooCmsAdmissionEducation(models.Model):
    _name = 'odoocms.admission.education'
    _description = 'Admission Education'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    degree_ids = fields.One2many('odoocms.admission.degree', 'admission_education_id', string='Degree')
