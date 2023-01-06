from datetime import date

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
    _name = 'odoocms.campus'
    _description = 'CMS Campus'
    _inherit = ['mail.thread','mail.activity.mixin']
    
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', help='Campus City Code')
    effective_date = fields.Date(string='Effective Date', help='Effective Date of Campus')
    active = fields.Boolean('Active', default=True, help="Current Status of Course")
    description = fields.Text(string='Description', help="Description about the Campus")
    short_description = fields.Text(string='Short Description', help="Short Description about the Campus")
    formal_description = fields.Text(string='Formal Description', help="Formal Description about the Campus")
    street = fields.Char(string='Address 1')
    street2 = fields.Char(string='Address 2')
    zip = fields.Char(change_default=True)
    city = fields.Char('City')
    country_id = fields.Many2one('res.country', string='Country', ondelete='cascade')
    company_id = fields.Many2one('res.company', string='Company')
    institute_ids = fields.One2many('odoocms.institute', 'campus_id', string='Institutes')
    to_be = fields.Boolean(default=False)
    
    def unlink(self):
        for rec in self:
            raise ValidationError(_("Academic Session can not be deleted, You only can Archive it."))
        
    _sql_constraints = [
        ('code', 'unique(code)', "Campus Code already exists."),
        ('name', 'unique(name)', "Campus Name already exists."),
    ]

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            recs = self.search([('name', operator, name)] + (args or []), limit=limit)
            if not recs:
                recs = self.search([('code', operator, name)] + (args or []), limit=limit)
            return recs.name_get()
        return super().name_search(name, args=args, operator=operator, limit=limit)


class OdooCMSInstitute(models.Model):
    _name = 'odoocms.institute'
    _description = 'CMS Institute'
    _inherit = ['mail.thread', 'mail.activity.mixin','image.mixin']

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True, help='Institute City Code')
    effective_date = fields.Date(string='Effective Date', help='Effective Date of Institute')
    active = fields.Boolean('Active', default=True, help="Current Status of Institute")
    website = fields.Char(string='Website')
    phone = fields.Char(string='Phone')

    department_ids = fields.One2many('odoocms.department', 'institute_id', string='Departments')
    campus_id = fields.Many2one('odoocms.campus', string='Campus')

    parent_id = fields.Many2one('odoocms.institute', string='Parent Institute')
    child_ids = fields.One2many('odoocms.institute', 'parent_id', string='SubInstitutes',
        domain=[('active', '=', True)])
    
    to_be = fields.Boolean(default=False)
    
    _sql_constraints = [
        ('code', 'unique(code)', "Institute Code already exists."),
        ('name', 'unique(name)', "Institute Name already exists."),
    ]

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            recs = self.search([('name', operator, name)] + (args or []), limit=limit)
            if not recs:
                recs = self.search([('code', operator, name)] + (args or []), limit=limit)
            return recs.name_get()
        return super().name_search(name, args=args, operator=operator, limit=limit)
    
      
class OdooCMSDepartment(models.Model):
    _name = 'odoocms.department'
    _description = 'CMS Department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string="Name", help="Department Name", required=True)
    code = fields.Char(string="Code", help="Department Code", required=True)
    effective_date = fields.Date(string="Effective Date", help="Effective Date", required=True)
    color = fields.Integer(string='Color Index')
    active = fields.Boolean('Active', default=True, help="Current Status of Department")
    
    program_ids = fields.One2many('odoocms.program', 'department_id', string="Programs")
    institute_id = fields.Many2one("odoocms.institute", string="Institute")
    campus_id = fields.Many2one('odoocms.campus','Campus', related='institute_id.campus_id',store=True)
    to_be = fields.Boolean(default=False)
    
    _sql_constraints = [
        ('code', 'unique(code)', "Department Code already exists."),
        ('name', 'unique(name)', "Department Name already exists."),
    ]

    def name_get(self):
        res = []
        for record in self:
            name = record.name
            if record.institute_id:
                name = name + ' - ' + record.institute_id.code or ''
            res.append((record.id, name))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            recs = self.search([('name', operator, name)] + (args or []), limit=limit)
            if not recs:
                recs = self.search([('code', operator, name)] + (args or []), limit=limit)
            return recs.name_get()
        return super().name_search(name, args=args, operator=operator, limit=limit)
 

class OdooCMSProgram(models.Model):
    _name = "odoocms.program"
    _description = "CMS Program"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    short_code = fields.Char('Short Code',size=4)
    color = fields.Integer(string='Color Index')
    duration = fields.Char('Duration')
    credits = fields.Integer('Credit Hours')
    effective_date = fields.Date(string="Effective Date", help="Effective Date", required=True)
    description = fields.Text(string='Formal Description')
    active = fields.Boolean('Active', default=True,
                            help="Current Status of Department")
    department_id = fields.Many2one('odoocms.department', string="Department")
    career_id = fields.Many2one('odoocms.career', string="Career")
    discipline_id = fields.Many2one('odoocms.discipline', string="Discipline")
    institute_id = fields.Many2one("odoocms.institute", string="Institute",related='department_id.institute_id',store=True)
    campus_id = fields.Many2one('odoocms.campus',string='Campus', related='institute_id.campus_id',store=True)
    
    specialization_ids = fields.One2many('odoocms.specialization', 'program_id', string='Specializations')
    to_be = fields.Boolean(default=False)
    
    _sql_constraints = [
        ('code', 'unique(code)', "Code already exists!"),
    ]

    def name_get(self):
        res = []
        for record in self:
            name = record.name
            if record.department_id:
                name = name + ' - ' + (record.department_id.institute_id and record.department_id.institute_id.code or '')
            res.append((record.id, name))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name:
            recs = self.search([('name', operator, name)] + (args or []), limit=limit)
            if not recs:
                recs = self.search([('code', operator, name)] + (args or []), limit=limit)
            return recs.name_get()
        return super().name_search(name, args=args, operator=operator, limit=limit)


class OdooCMSSpecialization(models.Model):
    _name = "odoocms.specialization"
    _description = "CMS Specialization"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    description  = fields.Text(string='Formal Description')
    program_id = fields.Many2one('odoocms.program', string='Program')
    

class ResCompany(models.Model):
    _inherit = "res.company"
    
    identifier = fields.Char('Import Identifier')
    
    

        
    
