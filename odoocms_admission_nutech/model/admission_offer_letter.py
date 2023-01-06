import pdb
from odoo import fields, models, _, api


class SuffaOfferLetter(models.Model):
    _name = 'admission.offer.letter'
    _description = 'Admission Offer Letter'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'applicant_id'

    applicant_id = fields.Many2one('odoocms.application', string='Name')
    program_id = fields.Many2one('odoocms.program', string='Program')
    reference_no = fields.Char(string='Reference No')
    date = fields.Datetime(string='Date')
