from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning


class OdooCMSApplicationMainSteps(models.Model):
    _name = 'odoocms.application.main.steps'
    _description = 'Application Main Steps'

    name = fields.Char('Step Name', required=True)
    step_no = fields.Integer('Step No', required=True)
    sequence = fields.Integer('Sequence')
    application_step_ids = fields.One2many('odoocms.application.steps', 'main_step_id', string='Application Steps')

    @api.model
    def create(self, values):
        record = super(OdooCMSApplicationMainSteps, self).create(values)
        if not record.sequence:
            record.sequence = self.env['ir.sequence'].next_by_code('application.main.steps')
        return record
