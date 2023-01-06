from odoo import models, fields


class EducationInstitute(models.Model):
    _name = 'odoocms.application.institute.school'
    _description = 'Educational Institute School'

    name = fields.Char(string='Odoo CMS Institute')
    code = fields.Char('code')


class EducationInstitute(models.Model):
    _name = 'odoocms.application.institute.college'
    _description = 'Educational Institute College'

    name = fields.Char(string='Odoo CMS Institute')
    code = fields.Char('code')


class EducationInstitute(models.Model):
    _name = 'odoocms.application.institute.university'
    _description = 'Educational Institute University '

    name = fields.Char(string='Odoo CMS Institute')
    code = fields.Char('code')
