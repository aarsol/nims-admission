from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, Warning


class OdooCMSApplicationSteps(models.Model):
    _name = 'odoocms.application.steps'
    _description = 'Application Steps'
    _order = 'sequence'

    name = fields.Char('Step Name', required=True)
    sequence = fields.Integer('Sequence', required=True)
    template = fields.Many2one('ir.ui.view', 'Template', required=True, domain=[
                               ('type', '=', 'qweb')])
    test_field = fields.Many2one('ir.model.fields', 'Completion Test Field', domain=[
                                 ('model', '=', 'odoocms.application')])
    career_ids = fields.Many2many(
        'odoocms.career', 'career_step_rel', 'career_id', 'step_id', 'Career')
    invisible = fields.Char()
    icon = fields.Char('Icon Unicode')
    step_details = fields.Html('Step Details')
    active = fields.Boolean(default=True)
    main_step_id = fields.Many2one('odoocms.application.main.steps', string='Main Steps')
    
