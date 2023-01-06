from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import pdb


class OdooCMSSectionPattern(models.Model):
    _name = "odoocms.section.pattern"
    _description = "CMS Section Pattern"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Pattern Name', required=True)
    sequence = fields.Integer('Sequence')
    active = fields.Boolean(default=True)
    line_ids = fields.One2many('odoocms.section.pattern.line','pattern_id')
    

class OdooCMSSectionPatternLine(models.Model):
    _name = "odoocms.section.pattern.line"
    _description = "CMS Section Pattern Line"
    
    name = fields.Char(string='Section Name', required=True)
    sequence = fields.Integer('Sequence')
    pattern_id = fields.Many2one('odoocms.section.pattern','Section Pattern')
    
    
class OdooCMSBatch(models.Model):
    _name = 'odoocms.batch'
    _description = "Program Batches"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence'

    name = fields.Char(string='Name', compute='_get_name_code', store=True)
    code = fields.Char(string="Code", compute='_get_name_code', store=True)
    
    sequence = fields.Integer('Sequence',default=10)
    color = fields.Integer(string='Color Index')
    department_id = fields.Many2one('odoocms.department', string="Department/Center", required=True)
    institute_id = fields.Many2one("odoocms.institute", string="Institute",related='department_id.institute_id',store=True)
    career_id = fields.Many2one('odoocms.career', string="Career/Degree Level", required=True)
    program_id = fields.Many2one('odoocms.program', string="Program", required=True)
    session_id = fields.Many2one('odoocms.academic.session', 'Calendar Year', required=True)
    
    term_id = fields.Many2one('odoocms.academic.term', 'Current Term')   # needs to remove
    semester_id = fields.Many2one('odoocms.semester', 'Semester')   # needs to remove
    
    term_line = fields.Many2one('odoocms.academic.term.line','Term Schedule',compute='get_term_line',store=True)    # need update in function by passing term_id
    user_ids = fields.Many2many('res.users', 'batch_user_access_rel', 'batch_id', 'user_id', 'Users', domain="[('share','=', False)]")

    building_id = fields.Many2one('odoocms.building', 'Building')
    floor_ids = fields.Many2many('odoocms.building.floor','batch_floor_rel','batch_id','floor_id','Floors')
    room_type = fields.Many2one('odoocms.room.type', 'Room Type')
    room_ids = fields.Many2many('odoocms.room', 'batch_room_rel', 'bath_id', 'room_id', 'Rooms')
    
    study_scheme_id = fields.Many2one('odoocms.study.scheme', 'Study Scheme', required=True)
    to_be = fields.Boolean(default=False)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name', 'unique(name)', "Name already exists for some other Batch!"),
        ('code', 'unique(code)', "Code already exists for some other Batch!"),
    ]
    
    @api.depends('program_id', 'session_id')
    def _get_name_code(self):
        for rec in self:
            if rec.program_id and rec.session_id:
                batch_code = rec.program_id.code + '-' + rec.session_id.code
                rec.code = batch_code
                rec.name = batch_code

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            recs = self.search([('name', operator, name)] + (args or []), limit=limit)
            if not recs:
                recs = self.search([('code', operator, name)] + (args or []), limit=limit)
            return recs.name_get()
        return super().name_search(name, args=args, operator=operator, limit=limit)
        
    @api.depends('term_id.term_lines')
    def get_term_line(self):
        for batch in self:
            term_line = self.env['odoocms.academic.term.line']
            for rec in batch.term_id.term_lines.sorted(key=lambda s: s.sequence,reverse=False):
                term_line = rec
                if rec.campus_ids and batch.program_id.campus_id not in rec.campus_ids:
                    continue
                elif rec.institute_ids and batch.program_id.department_id.institute_id not in rec.institute_ids:
                    continue
                elif rec.career_ids and batch.career_id not in rec.career_ids:
                    continue
                elif rec.program_ids and batch.program_id not in rec.program_ids:
                    continue
                elif rec.batch_ids and batch not in rec.batch_ids:
                    continue
                else:
                    break
            batch.term_line = term_line and term_line.id or False

    def getermline(self, term_id):
        batch = self.sudo()
        term_line = self.env['odoocms.academic.term.line']
        for rec in term_id.term_lines.sorted(key=lambda s: s.sequence, reverse=False).sudo():
            term_line = rec
            if rec.campus_ids and batch.program_id.campus_id not in rec.campus_ids:
                continue
            elif rec.institute_ids and batch.program_id.department_id.institute_id not in rec.institute_ids:
                continue
            elif rec.career_ids and batch.career_id not in rec.career_ids:
                continue
            elif rec.program_ids and batch.program_id not in rec.program_ids:
                continue
            elif rec.batch_ids and batch not in rec.batch_ids:
                continue
            else:
                break
        return term_line
            
    def can_apply(self, event, term_id=None, date_request =None, admin=False):
        today = date.today() if not date_request else date_request
        can_apply = False
        term_line = self.getermline(term_id) if term_id else self.term_line
        planning_id = term_line.planning_ids.filtered(lambda l: l.type == event)
        if planning_id and (planning_id.date_start <= today <= planning_id.date_end):
            can_apply = True
        if admin and planning_id:
            date_start = planning_id.date_start_admin or planning_id.date_start
            date_end = planning_id.date_end_admin or planning_id.date_end
            if date_start <= today <= date_end:
                can_apply = True
        return can_apply


