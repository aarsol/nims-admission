from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import pdb


class OdooCMSDiscipline(models.Model):
    _name = 'odoocms.discipline'
    _description = 'CMS Discipline'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Discipline", help="Discipline Name")
    code = fields.Char(string="Code", help="Discipline Code")
    description = fields.Text(string='Description', help="Short Description about the Discipline")
    program_ids = fields.One2many('odoocms.program','discipline_id','Academic Programs')
    
    _sql_constraints = [
        ('code', 'unique(code)', "Code already exists!"),
    ]


class OdooCMSCampus(models.Model):
    _inherit = 'odoocms.campus'
    
    faculty_ids = fields.One2many('odoocms.department.line', 'campus_id', string="Faculty")
    
    # need to check either it is required
    no_registration_tag_ids = fields.Many2many('odoocms.student.tag', 'campus_no_registration_tag_rel', 'campus_id', 'tag_id', 'No Registration Tags')

    
class OdooCMSInstitute(models.Model):
    _inherit = 'odoocms.institute'
    
    faculty_ids = fields.One2many('odoocms.department.line', 'institute_id', string="Faculty")
    
      
class OdooCMSDepartment(models.Model):
    _inherit = 'odoocms.department'
    
    faculty_ids = fields.One2many('odoocms.department.line', 'department_id', string="Faculty")
    hod_id = fields.Many2one("hr.employee", string="HOD")
    

class OdooCMSDepartmentLineTag(models.Model):
    _name = 'odoocms.department.line.tag'
    _description = 'Department/Center Line Tag'

    name = fields.Char(string="Faculty Tag", required=True)
    color = fields.Integer(string='Color Index')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', "Tag name already exists !"),
    ]
    
    
class OdooCMSDepartmentLine(models.Model):
    _name = 'odoocms.department.line'
    _description = 'CMS Department Line'
    
    department_id = fields.Many2one('odoocms.department',string='Department/Center')
    
    faculty_staff_id = fields.Many2one('odoocms.faculty.staff',string='Faculty Staff') # unused
    
    institute_id = fields.Many2one('odoocms.institute','Institute',related='department_id.institute_id',store=True,readonly=False)
    campus_id = fields.Many2one('odoocms.campus', 'Campus', related='institute_id.campus_id', store=True,readonly=False)
    
    employee_id = fields.Many2one('hr.employee',string='Employee')
    employee_name = fields.Char(related = 'employee_id.name', store=True,string='Employee Name')
    employee_work_phone = fields.Char(related = 'employee_id.work_phone', store=True,string='Work Phone')
    employee_work_email = fields.Char(related = 'employee_id.work_email', store=True,string='Work Email')
    employee_department_id = fields.Many2one(related = 'employee_id.department_id', store=True,string='HR Department')
    employee_job_id = fields.Many2one(related = 'employee_id.job_id', store=True,string='Job Position')
    employee_parent_id = fields.Many2one(related = 'employee_id.parent_id', store=True,string='Manager')
    employee_tag_id = fields.Many2many('odoocms.department.line.tag','department_line_tag_rel','department_line_id','tag_id','Tags')
    

class OdooCMSProgram(models.Model):
    _inherit = "odoocms.program"
    
    reg_code = fields.Char('Registration Code')
    building_id = fields.Many2one('odoocms.building','Building')
    floor_ids = fields.Many2many('odoocms.building.floor','program_floor_rel','program_id','floor_id','Floors')
    room_type = fields.Many2one('odoocms.room.type', 'Room Type')
    room_ids = fields.Many2many('odoocms.room','program_room_rel','program_id','room_id','Rooms')
    
    # specialization_ids = fields.One2many('odoocms.specialization', 'program_id', string='Specializations')
    batch_ids = fields.One2many('odoocms.batch', 'program_id', string='Batches')
    repeat_grades_allowed = fields.Char(string="Repeat Grades Allowed")
    deficient_course_in_summer = fields.Boolean(string="Deficient Course in Summer?")
    advance_course_in_summer = fields.Boolean(string="Advance Course in Summer?")
    user_ids = fields.Many2many('res.users', 'program_user_access_rel', 'program_id', 'user_id', 'Users', domain="[('share','=', False)]")
    tracking_ids = fields.One2many('odoocms.program.user.tracking','program_id','Coordinator Tracking')
    
    def write(self, vals):
        removed_users = self.env['res.users']
        added_users = self.env['res.users']
        if vals.get('user_ids',False):
            updated_users = self.env['res.users'].search([('id','in',vals.get('user_ids')[0][2])])
            added_users = updated_users - self.user_ids
            removed_users = self.user_ids - updated_users

        result = super(OdooCMSProgram, self).write(vals)
        for added_user in added_users:
            if added_user.has_group('odoocms.group_cms_coordinator'):
                data = {
                    'program_id': self.id,
                    'action': 'Added',
                    'action_by': self.env.user.id,
                    'user_id': added_user.id,
                    'track_time': fields.Datetime.now(),
                }
                self.env['odoocms.program.user.tracking'].create(data)
        for removed_user in removed_users:
            if removed_user.has_group('odoocms.group_cms_coordinator'):
                data = {
                    'program_id': self.id,
                    'action': 'Removed',
                    'action_by': self.env.user.id,
                    'user_id': removed_user.id,
                    'track_time': fields.Datetime.now(),
                }
                self.env['odoocms.program.user.tracking'].create(data)
            
        return result
    

class ProgramUserTracking(models.Model):
    _name = 'odoocms.program.user.tracking'
    _description = 'Program User Tracking'

    program_id = fields.Many2one('odoocms.program', 'Program',required=True)
    action = fields.Char('Action',required=True)
    action_by = fields.Many2one('res.users', 'Action By',required=True)
    user_id = fields.Many2one('res.users', 'User',required=True)
    track_time = fields.Datetime('Track Time')
    date_start = fields.Date('Date Start')
    date_end = fields.Date('Date End')
    
   
class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    code = fields.Char(string="Code")


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.onchange('user_id')
    def onchange_user(self):
        if self.user_id:
            self.work_email = self.user_id.email
            self.identification_id = False
            self.user_id.employee_id = self.id
            fs_id = self.env['odoocms.faculty.staff'].search([('employee_id', '=', self.id)])
            if fs_id:
                self.user_id.faculty_staff_id = fs_id.id
    
    @api.onchange('address_id')
    def onchange_address_id(self):
        if self.address_id:
            self.work_phone = self.address_id.phone
            self.mobile_phone = self.address_id.mobile

    def write(self, vals):
        auto = vals.get('auto', False)
        if auto:
            del vals['auto']
        res = super().write(vals)
        if vals.get('user_id', False) and not auto:
            self.user_id.write({
                'user_type': self._context.get('user_type','employee'),
                'employee_id': self.id,
                'auto': True,
            })
        return res
    

class ResCompany(models.Model):
    _inherit = "res.company"
    
    identifier = fields.Char('Import Identifier')
    
    
class ResUsers(models.Model):
    _inherit = "res.users"
    
    user_type = fields.Selection([('faculty', 'Faculty'), ('student', 'Student'), ('employee', 'Employee')], 'User Type', default='employee')
    student_id = fields.Many2one('odoocms.student', 'Student')
    faculty_staff_id = fields.Many2one('odoocms.faculty.staff','Faculty Staff')
    employee_id = fields.Many2one('hr.employee','Related Employee')
    program_ids = fields.Many2many('odoocms.program', 'program_user_access_rel', 'user_id', 'program_id', 'Programs')
    batch_ids = fields.Many2many('odoocms.batch', 'batch_user_access_rel', 'user_id', 'batch_id', 'Batches')

    def write(self, vals):
        auto = vals.get('auto', False)
        if auto:
            del vals['auto']
        if vals.get('user_type', False):
            if vals.get('user_type') == 'student':
                vals['employee_id'] = False
                vals['faculty_staff_id'] = False
            if vals.get('user_type') == 'faculty':
                vals['employee_id'] = False
                vals['student_id'] = False
            if vals.get('user_type') == 'employee':
                vals['student_id'] = False
                vals['faculty_staff_id'] = False
        
        res = super().write(vals)
        if vals.get('student_id', False) and not auto:
            self.student_id.with_context(user_type='student').write({
                'user_id': self.id,
                'auto': True,
            })
        elif vals.get('faculty_staff_id', False) and not auto:
            #self.faculty_staff_id.employee_id.resource_id.user_id = self.id
            self.faculty_staff_id.with_context(user_type='faculty').write({
                'user_id': self.id,
                'auto': True,
            })
        elif vals.get('employee_id', False) and not auto:
            #self.employee_id.resource_id.user_id = self.id
            self.employee_id.with_context(user_type='employee').write({
                'user_id': self.id,
                'auto': True,
            })
        
        return res

        
    
