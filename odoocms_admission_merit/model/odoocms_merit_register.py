import pdb

from odoo import fields, models, _, api


class OdooCmsMeritRegister(models.Model):
    _name = 'odoocms.merit.registers'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Odoo Cms Merit Register'

    name = fields.Char(string='Name')
    register_id = fields.Many2one(
        'odoocms.admission.register', string='Register')
    merit_register_ids = fields.One2many(
        'odoocms.merit.register.line', 'merit_reg_id')
    ssc_aggregate_percent = fields.Float(
        string='SSC Aggregate Percent', default=0)
    hssc_aggregate_percent = fields.Float(
        string='HSSC Aggregate Percent', default=0)
    program_id = fields.Many2one('odoocms.program', string='Program')
    entry_test_aggregate_percent = fields.Float(
        string='Entry Test Aggregate Percent', default=0)
    pre_test_aggregate_percent = fields.Float(
        string='Pre Test Aggregate Percent', default=0)
    publish_merit = fields.Boolean(string='Publish Merit', default=False)
    program_ids = fields.One2many(
        'odoocms.merit.program', 'merit_register_id', string='Program')
    merit_agg_ids = fields.One2many('odoocms.merit.test.aggregate', 'merit_reg_id')
    # pre_test_agg_ids = fields.One2many('odoocms.merit.pre.test.aggregate', 'merit_reg_id')
    state = fields.Selection(
        string='State',
        selection=[('draft', 'Draft'),
                   ('open', 'Open'), ('done', 'Done'), ],
        required=False, default='draft')

    def calculate_merit(self):
        for rec in self:
            rec.merit_register_ids.unlink()
            rec.merit_agg_ids.unlink()
            applicants = self.env['applicant.entry.test'].search(
                [('state', '=', True)])
            for app in applicants:
                ssc_per = 0
                inter_per = 0
                for student_merit in app.student_id.applicant_academic_ids:
                    if student_merit.degree_name.name in ('Matric', 'O-Level'):
                        ssc_percentage = (
                                                 student_merit.obt_marks / student_merit.total_marks) * 100
                        ssc_per = float("{:.2f}".format(ssc_percentage))

                    elif student_merit.degree_name.name in ('Intermediate', 'A-Level', 'DAE'):
                        inter_percentage = (
                                                   student_merit.obt_marks / student_merit.total_marks) * 100
                        inter_per = float("{:.2f}".format(inter_percentage))

                partial_agg = 0
                for app_agg in app.applicant_line_ids.sorted(key=lambda r: r.name):
                    for agg_rec in rec.merit_agg_ids.sorted(key=lambda r: r.name):
                        if app_agg.name == agg_rec.name:
                            partial_agg = partial_agg + (((app_agg.obtained_marks / app_agg.total_marks) * 100) * (
                                    agg_rec.aggregate / 100))

                total_aggregate = ((rec.ssc_aggregate_percent / 100) * (ssc_per)) + (
                        (rec.hssc_aggregate_percent / 100) * (inter_per)) + partial_agg

                for merit_program in rec.program_ids:
                    if merit_program.program_id.id == app.entry_test_schedule_details_id.program_id.id and app.entry_test_marks > 0:
                        merit_line = self.env['odoocms.merit.register.line'].sudo().create({
                            'merit_reg_id': rec.id,
                            'applicant_id': app.student_id.id,
                            'aggregate': total_aggregate,
                            'program_id': app.entry_test_schedule_details_id.program_id.id,
                            'public_visible': True,
                            'selected': True,
                        })
                    rec.state = 'open'
                    app.section_wise_marks()

                # this loop is based on of model order_by program_id and aggregate
                program_app = []
                for merit in rec.merit_register_ids:
                    categorized_merit = merit.search(
                        [('program_id', '=', merit.program_id.id), ('merit_reg_id', '=', rec.id)])
                    merit_no = 1
                    for cm in categorized_merit:
                        if merit.program_id.id not in program_app:
                            program_app.append(merit.program_id.id)
                        cm.merit_no = merit_no
                        merit_no += 1

            # Test Aggregate Group
            for aggregate_program in rec.program_ids:
                admit_card = self.env['applicant.entry.test'].search(
                    [('entry_test_schedule_details_id.program_id', '=', aggregate_program.program_id.id)], limit=1)
                for admit_line in admit_card.applicant_line_ids:
                    merit_line = self.env['odoocms.merit.test.aggregate'].sudo().create({
                        'merit_reg_id': self.id,
                        'program_id': admit_card.entry_test_schedule_details_id.program_id.id,
                        'name': admit_line.name,
                    })

    def submit(self):
        for rec in self:
            rec.publish_merit = True
            rec.state = 'done'

    def generate_offer_letter(self):
        for rec in self:
            if rec.publish_merit == True:
                for offer in rec.merit_register_ids:
                    offer_letter = self.env['admission.offer.letter'].search([])
                    offer_letter.create({
                        'applicant_id': offer.applicant_id.id,
                        'program_id': offer.program_id.id,
                    })


class OdooCmsMeritRegister(models.Model):
    _name = 'odoocms.merit.register.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'program_id , aggregate desc'
    _rec_name = 'applicant_id'
    _description = 'Odoo Cms Merit Register Line'

    merit_no = fields.Integer(string='Merit No')
    aggregate = fields.Float(string='Aggregate')
    applicant_id = fields.Many2one('odoocms.application', string='Application')
    applicant = fields.Char( related='applicant_id.name', string='Applicant Name', store=True)
    reference_no = fields.Char( related='applicant_id.application_no', string='Reference No',  store=True)
    merit_reg_id = fields.Many2one('odoocms.merit.registers')
    program_id = fields.Many2one('odoocms.program', string='Program')
    public_visible = fields.Boolean(string='Public Visible')
    selected = fields.Boolean(string='Selected')
    matric_marks = fields.Integer(
        string='Matric Marks', compute='_get_matric_marks', store=True)
    inter_marks = fields.Integer(
        string='Inter Marks', compute='_get_inter_marks', store=True)
    entry_test_marks = fields.Integer(string='Entry Test Marks')
    pre_test_marks = fields.Integer(string='Pre Test Marks', compute='_get_pre_test_marks', store=True)
    cbt_english = fields.Integer(string='English Marks', compute='_get_cbt_eng_marks', store=True)
    cbt_t_english = fields.Integer(string='Total English Marks')
    cbt_per_english = fields.Integer(string='Precentage English')
    cbt_math = fields.Integer(string='Mathematics Marks', compute='_get_cbt_math_marks', store=True)
    cbt_t_math = fields.Integer(string='Total Mathematics Marks')
    cbt_per_math = fields.Integer(string='Percentage Mathematics')
    cbt_physics = fields.Integer(string='Physics Marks', compute='_get_cbt_phy_marks', store=True)
    cbt_t_physics = fields.Integer(string='Total Physics Marks')
    cbt_per_physics = fields.Integer(string='Percentage Physics')
    cbt_chemistry = fields.Integer(string='Chemistry Marks', compute='_get_cbt_chem_marks', store=True)
    cbt_t_chemistry = fields.Integer(string='Total Chemistry Marks')
    cbt_per_chemistry = fields.Integer(string='Percentage Chemistry')
    cbt_analytical = fields.Integer(string='Analytical Marks', compute='_get_cbt_analy_marks', store=True)
    cbt_t_analytical = fields.Integer(string='Total Analytical Marks')
    cbt_per_analytical = fields.Integer(string='Percentage Analytical')
    cbt_bio = fields.Integer(string='Biology Marks', compute='_get_cbt_bio_marks', store=True)
    cbt_t_bio = fields.Integer(string='Total Biology Marks')
    cbt_per_bio = fields.Integer(string='Percentage Biology')
    cbt_rc = fields.Integer(string='Reading Comprehension', compute='_get_cbt_rc_marks', store=True)
    cbt_t_rc = fields.Integer(string='Total Reading Comprehension')
    cbt_per_rc = fields.Integer(string='Precentage Reading Comprehension')
    cbt_ew = fields.Integer(string='Essay Writing', compute='_get_cbt_ew_marks', store=True)
    cbt_t_ew = fields.Integer(string='Total Essay Writing')
    cbt_per_ew = fields.Integer(string='Percentage Essay Writing')
    cbt_obtained = fields.Integer(string='CBT Obtained Marks', compute='_get_cbt_obtained_marks', store=True)
    cbt_total = fields.Integer(string='CBT Total Marks')
    cbt_percentage = fields.Integer(string='CBT Percentage')
    cbt_section_ids = fields.One2many('cbt.section.marks', 'merit_line_id')
    cbt_aggregate_ids = fields.One2many('cbt.test.aggregate', 'merit_line_id')

    @api.depends('applicant_id')
    def _get_cbt_eng_marks(self):
        for rec in self:
            rec.cbt_english = 0
            applicant_cbt_id = self.env['applicant.entry.test'].search(
                [('student_id', '=', rec.applicant_id.id)])
            for cbt_sec in applicant_cbt_id.applicant_line_ids:
                if cbt_sec.name == 'English':
                    rec.cbt_english = cbt_sec.obtained_marks
                    rec.cbt_t_english = cbt_sec.total_marks
                    if rec.cbt_total:
                        rec.cbt_per_english = round((cbt_sec.obtained_marks/cbt_sec.total_marks)*100,2)

    @api.depends('applicant_id')
    def _get_cbt_obtained_marks(self):
        for rec in self:
            rec.cbt_obtained = 0
            applicant_cbt_id = self.env['applicant.entry.test'].search(
                [('student_id', '=', rec.applicant_id.id)])
            # for app in applicant_cbt_id:
            rec.cbt_obtained = applicant_cbt_id.entry_test_marks
            for cbt_sec in applicant_cbt_id.applicant_line_ids:
                rec.cbt_total += cbt_sec.total_marks
            if rec.cbt_total:
                rec.cbt_percentage = round((rec.cbt_obtained/rec.cbt_total)*100,2)



    @api.depends('applicant_id')
    def _get_cbt_math_marks(self):
        for rec in self:
            rec.cbt_math = 0
            applicant_cbt_id = self.env['applicant.entry.test'].search(
                [('student_id', '=', rec.applicant_id.id)])
            for cbt_sec in applicant_cbt_id.applicant_line_ids:
                if cbt_sec.name == 'Mathematics':
                    rec.cbt_math = cbt_sec.obtained_marks
                    rec.cbt_t_math = cbt_sec.total_marks
                    if cbt_sec.total_marks:
                        rec.cbt_per_math = round((cbt_sec.obtained_marks / cbt_sec.total_marks) * 100, 2)

    @api.depends('applicant_id')
    def _get_cbt_phy_marks(self):
        for rec in self:
            rec.cbt_physics = 0
            applicant_cbt_id = self.env['applicant.entry.test'].search(
                [('student_id', '=', rec.applicant_id.id)])
            for cbt_sec in applicant_cbt_id.applicant_line_ids:
                if cbt_sec.name == 'Physics':
                    rec.cbt_physics = cbt_sec.obtained_marks
                    rec.cbt_t_physics = cbt_sec.total_marks
                    if cbt_sec.total_marks:
                        rec.cbt_per_physics = round((cbt_sec.obtained_marks / cbt_sec.total_marks) * 100, 2)

    @api.depends('applicant_id')
    def _get_cbt_chem_marks(self):
        for rec in self:
            rec.cbt_chemistry = 0
            applicant_cbt_id = self.env['applicant.entry.test'].search(
                [('student_id', '=', rec.applicant_id.id)])
            for cbt_sec in applicant_cbt_id.applicant_line_ids:
                if cbt_sec.name == 'Chemistry':
                    rec.cbt_chemistry = cbt_sec.obtained_marks
                    rec.cbt_t_chemistry = cbt_sec.total_marks
                    if cbt_sec.total_marks:
                        rec.cbt_per_chemistry = round((cbt_sec.obtained_marks / cbt_sec.total_marks) * 100, 2)

    @api.depends('applicant_id')
    def _get_cbt_analy_marks(self):
        for rec in self:
            rec.cbt_analytical = 0
            applicant_cbt_id = self.env['applicant.entry.test'].search(
                [('student_id', '=', rec.applicant_id.id)])
            for cbt_sec in applicant_cbt_id.applicant_line_ids:
                if cbt_sec.name == 'Analytical':
                    rec.cbt_analytical = cbt_sec.obtained_marks
                    rec.cbt_t_analytical = cbt_sec.total_marks
                    if cbt_sec.total_marks:
                        rec.cbt_per_analytical = round((cbt_sec.obtained_marks / cbt_sec.total_marks) * 100, 2)


    @api.depends('applicant_id')
    def _get_cbt_bio_marks(self):
        for rec in self:
            rec.cbt_bio = 0
            applicant_cbt_id = self.env['applicant.entry.test'].search(
                [('student_id', '=', rec.applicant_id.id)])
            for cbt_sec in applicant_cbt_id.applicant_line_ids:
                if cbt_sec.name == 'Biology':
                    rec.cbt_bio = cbt_sec.obtained_marks
                    rec.cbt_t_bio = cbt_sec.total_marks
                    if cbt_sec.total_marks:
                        rec.cbt_per_bio = round((cbt_sec.obtained_marks / cbt_sec.total_marks) * 100, 2)

    @api.depends('applicant_id')
    def _get_cbt_rc_marks(self):
        for rec in self:
            rec.cbt_rc = 0
            applicant_cbt_id = self.env['applicant.entry.test'].search(
                [('student_id', '=', rec.applicant_id.id)])
            for cbt_sec in applicant_cbt_id.applicant_line_ids:
                if cbt_sec.name == 'Reading Comprehension':
                    rec.cbt_rc = cbt_sec.obtained_marks
                    rec.cbt_t_rc = cbt_sec.total_marks
                    if cbt_sec.total_marks:
                        rec.cbt_per_rc = round((cbt_sec.obtained_marks / cbt_sec.total_marks) * 100, 2)

    @api.depends('applicant_id')
    def _get_cbt_ew_marks(self):
        for rec in self:
            rec.cbt_ew = 0
            applicant_cbt_id = self.env['applicant.entry.test'].search(
                [('student_id', '=', rec.applicant_id.id)])
            for cbt_sec in applicant_cbt_id.applicant_line_ids:
                if cbt_sec.name == 'Essay Writing':
                    rec.cbt_ew = cbt_sec.obtained_marks
                    rec.cbt_t_ew = cbt_sec.total_marks
                    if cbt_sec.total_marks:
                        rec.cbt_per_ew = round((cbt_sec.obtained_marks / cbt_sec.total_marks) * 100, 2)


    @api.depends('applicant_id.applicant_academic_ids')
    def _get_inter_marks(self):
        for rec in self:
            applicant_marks = self.env['odoocms.application'].search(
                [('id', '=', rec.applicant_id.id)])
            for marks in applicant_marks.applicant_academic_ids:
                if marks.degree_name.name in ('Intermediate', 'A-Level'):
                    obtained_marks = marks.obt_marks
                    rec.inter_marks = obtained_marks

    @api.depends('applicant_id.applicant_academic_ids')
    def _get_matric_marks(self):
        for rec in self:
            applicant_marks = self.env['odoocms.application'].search(
                [('id', '=', rec.applicant_id.id)])
            for marks in applicant_marks.applicant_academic_ids:
                if marks.degree_name.name in ('Matric', 'O-Level'):
                    obtained_marks = marks.obt_marks
                    rec.matric_marks = obtained_marks

    @api.depends('applicant_id.preference_ids')
    def _get_pre_test_marks(self):
        self.pre_test_marks = 0
        for rec in self:
            # application = self.env['odoocms.application'].search([('id', '=', rec.applicant_id.id)])
            # program = application.preference_ids[0].program_id
            # if program and program.pre_test:
            #     marks = application.pre_test_marks
            #     rec.pre_test_marks = marks
            application = self.env['odoocms.application'].search(
                [('id', '=', rec.applicant_id.id)])
            preference = application.preference_ids.filtered(
                lambda x: x.preference == 1).program_id
            preference_program = preference
            if preference and preference.pre_test:
                rec.pre_test_marks = application.pre_test_marks


class OdooCmsMeritAggregate(models.Model):
    _name = 'odoocms.merit.test.aggregate'
    _description = 'Odoo Cms Merit Aggregate'

    name = fields.Char(string='Name')
    aggregate = fields.Float(string='Aggregate')
    merit_reg_id = fields.Many2one(
        'odoocms.merit.registers', string='Merit Register')
    program_id = fields.Many2one('odoocms.program', string='Program', )


# class OdooCmsMeritAggregate(models.Model):
#     _name = 'odoocms.merit.pre.test.aggregate'
#     _description = 'Odoo Cms Pre Test Merit Aggregate'
#
#     pre_test_id = fields.Many2one('odoocms.pre.test', string='Name')
#     aggregate = fields.Float(string='Aggregate')
#     merit_reg_id = fields.Many2one(
#         'odoocms.merit.registers', string='Merit Register')


class OdoocmsMeritProgram(models.Model):
    _name = 'odoocms.merit.program'
    _description = 'Odoocms Merit Program'

    merit_register_id = fields.Many2one(
        'odoocms.merit.registers', 'Merit Register')
    program_id = fields.Many2one('odoocms.program', string='Program')


class CBTMarks(models.Model):
    _name = 'cbt.section.marks'
    _description = 'CBT Section Marks'

    name = fields.Char(string='Name')
    marks = fields.Integer(string='Obtained Marks')
    merit_line_id = fields.Many2one('odoocms.merit.register.line')


class CBTTestGroupAggregate(models.Model):
    _name = 'cbt.test.aggregate'
    _description = 'CBT Test Group Aggregate'

    name = fields.Char(string='Name')
    marks = fields.Integer(string='Marks')
    merit_line_id = fields.Many2one('odoocms.merit.register.line')
