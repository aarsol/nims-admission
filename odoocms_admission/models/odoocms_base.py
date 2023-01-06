from odoo import fields, models, api


class OdooCMSDegree(models.Model):
    _name = 'odoocms.degree'
    _description = 'Degree'

    name = fields.Char('Degree Name', required=True)
    code = fields.Char('Code', required=True)
    career_id = fields.Many2one('odoocms.career', string="Admission Career")
    sequence = fields.Integer('Sequence', default=10)
    active = fields.Boolean(default=True)
    # offering = fields.Boolean(string='Offering', default=True)
    program_ids = fields.Many2many('odoocms.program', 'program_degree_rel', 'degree_id', 'program_id', 'Programs')
    degree_id = fields.Many2one('odoocms.admission.degree', string='Degree', required=True)
    specialization_id = fields.Many2one('applicant.academic.group', string='Specialization/Group', required=True)
    eligibilty_percentage = fields.Float(string='Eligibility Percentage >=', )
    eligibilty_per = fields.Float(string='Eligibility Percentage <=', )
    eligibilty_cgpa = fields.Float(string='Eligibility CGPA >=', )
    eligibilty_cgp = fields.Float(string='Eligibility CGPA <=', )

    @api.onchange('degree_id')
    def onchange_institute_id(self):
        for rec in self:
            return {'domain': {'specialization_id': [('degree_id', '=', rec.degree_id.id)]}}


class OdooCMSProgram(models.Model):
    _inherit = "odoocms.program"

    degree_ids = fields.Many2many('odoocms.degree', 'program_degree_rel', 'program_id', 'degree_id', 'Degrees')
    # prospectus_fee_due_date = fields.Date(string='Prospectus Fee Due Date')
    prospectus_registration_fee = fields.Integer(string='Prospectus Fee', default=0)
    prospectus_program_fee_date = fields.Date(string='Prospectus Due Date')
    admission_due_date = fields.Date(string='Admission Due Date')
    signup_end_date = fields.Date(string='Sign up End Date')
    signin_end_date = fields.Date(string='Sign in End Date')
    commencement_class_date = fields.Date(string='Commencement of class date')
    pre_test = fields.Many2one('odoocms.pre.test', string='Pre Test')


class OdoocmsApplicationBoard(models.Model):
    _name = 'odoocms.application.board'
    _description = 'Education Board'

    name = fields.Char(string='Name', required=True)
    sh_name = fields.Char(string='Short Name')
    code = fields.Char('Code')
    city_id = fields.Many2one('odoocms.city', 'City')


class OdoocmsApplicationPassingYear(models.Model):
    _name = 'odoocms.application.passing.year'
    _description = 'Application Passing Year'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='code')
    matric = fields.Boolean('Matric', default=True)
    inter = fields.Boolean('Intermediate', default=True)
