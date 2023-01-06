import pdb

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)


class OdooCMSAcademicSession(models.Model):
    _name = 'odoocms.academic.session'
    _description = 'Academic Session'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence'

    def unlink(self):
        for rec in self:
            raise ValidationError(_("Academic Session can not be deleted, You only can Archive it."))

    def copy(self):
        for rec in self:
            raise ValidationError(_("Academic Session can not duplicated. Create a new One"))

    name = fields.Char(string='Name', required=1, help='Name of Academic Session')
    code = fields.Char(string='Code', required=1, help='Code of Academic Session')
    description = fields.Text(string='Description', help="Description about the Academic Session")
    sequence = fields.Integer(string='Sequence', required=True, default=10)
    
    active = fields.Boolean('Active', default=True,
                            help="If Unchecked, it will allow you to hide the Academic Session without removing it.")
    
    _sql_constraints = [
        ('code', 'unique(code)', "Code already exists for another Academic Session!"),
        ('name', 'unique(name)', "Name already exists for another Academic Session!"),
    ]


class OdooCMSAcademicTerm(models.Model):
    _name = 'odoocms.academic.term'
    _description = 'Academic Term'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence desc'
    
    def unlink(self):
        for rec in self:
            raise ValidationError(_("Academic Term can not be deleted, You only can Archive it."))

    name = fields.Char(string='Name', required=True, help='Name of Term',copy=False)
    code = fields.Char(string='Code', required=True, help='Code of Term', tracking=True,copy=False)
    sequence = fields.Integer(string='Sequence', required=True, default=50)
    short_code = fields.Char('Short Code',copy=False)
    number = fields.Integer('Number')
    type = fields.Selection([('regular', 'Regular'), ('summer', 'Summer'), ('special', 'Special')],
        string='Type', default='regular')
    
    enrollment_active = fields.Boolean('Enrollment Active?', default=False)
    current = fields.Boolean('Current Term', default=False)

    description = fields.Text(string='Description', help="Description about the Term")
    short_description = fields.Text(string='Short Description', help="Short Description about the Term")
    
    _sql_constraints = [
        ('code', 'unique(code)', "Code already exists for another Term!"),
        ('name', 'unique(name)', "Name already exists for another Term!"),
    ]

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            recs = self.search([('name', operator, name)] + (args or []), limit=limit)
            if not recs:
                recs = self.search([('code', operator, name)] + (args or []), limit=limit)
            return recs.name_get()
        return super(OdooCMSAcademicTerm, self).name_search(name, args=args, operator=operator, limit=limit)

    