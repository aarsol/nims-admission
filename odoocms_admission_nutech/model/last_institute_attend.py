import pdb

from odoo import fields, models, _, api


class LastInstituteAttend(models.Model):
    _name = 'last.institute.attend'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Last Institute Attend'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
