import pdb

from odoo import fields, models, _, api


class PreTest(models.Model):
    _name = 'odoocms.pre.test'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Pre Test'

    name = fields.Char(string='Test Name')
    code = fields.Char(string='Code')
    pre_test_total_marks = fields.Integer(string='Total Marks')
