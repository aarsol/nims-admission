from odoo import http, _, SUPERUSER_ID
from odoo.http import route, request, Controller, content_disposition
from odoo.exceptions import UserError, ValidationError
from werkzeug.datastructures import FileStorage
from datetime import date, datetime
import json
import base64
import pdb


class RegisterApplication(Controller):

    def _show_report_admit(self, model, report_type, report_ref, download=False):

        if report_type not in ('html', 'pdf', 'text'):
            raise UserError(_("Invalid report type: %s") % report_type)

        report_sudo = request.env.ref(report_ref).with_user(SUPERUSER_ID)

        if not isinstance(report_sudo, type(request.env['ir.actions.report'])):
            raise UserError(
                _("%s is not the reference of a report") % report_ref)

        method_name = '_render_qweb_%s' % (report_type)
        report = getattr(report_sudo, method_name)(
            [model.id], data={'report_type': report_type})[0]
        reporthttpheaders = [
            ('Content-Type', 'application/pdf' if report_type == 'pdf' else 'text/html'),
            ('Content-Length', len(report)),
        ]
        if report_type == 'pdf' and download:
            filename = "letter.pdf"
            reporthttpheaders.append(
                ('Content-Disposition', content_disposition(filename)))
        return request.make_response(report, headers=reporthttpheaders)

    @route('/admission/application/', type='http', auth='user', csrf=False, website=True, method=['GET', 'POST'])
    def admission_application(self, **kw):

        current_user = request.env.user

        # geting register , career and application can be tuned later for usage

        application_id = request.env['odoocms.application'].sudo().search(
            [('application_no', '=', current_user.login)])

        if not application_id:
            return http.request.redirect('/web/')

        # getting counry ,province , domicile , religion and steps of template
        country_id = request.env['res.country'].sudo().search([])
        province_id = request.env['odoocms.province'].sudo().search([])
        domicile_id = request.env['odoocms.domicile'].sudo().search([])
        city_id = request.env['odoocms.city'].sudo().search([])
        religion_id = request.env['odoocms.religion'].sudo().search([])
        profession_id = request.env['odoocms.profession'].sudo().search([])
        board_id = request.env['odoocms.application.board'].sudo().search([])
        passing_year = request.env['odoocms.application.passing.year'].sudo().search([
        ])
        academic_id = request.env['applicant.academic.detail'].sudo().search([
        ])
        undertaking = application_id.register_id.undertaking

        academic_data = request.env['odoocms.admission.education'].sudo().search([
        ])
        # need_base_scholarship = request.env['applicant.need.base.scholarship']
        # scholarship_need_base = request.env['applicant.need.base.scholarship'].sudo(
        # ).search([('application_id', '=', application_id.id)], limit=1)

        company = request.env['res.company'].sudo().search([])
        descipline_id = request.env['odoocms.discipline'].sudo().search([])
        center_id = application_id.register_id.test_series_ids
        # last_institute_attend = request.env['last.institute.attend'].sudo().search([
        # ])
        advertisement = request.env['odoocms.advertisement'].sudo().search([])

        steps_id = request.env['odoocms.application.steps'].sudo().search(
            [], order='sequence')

        # if not register_id:
        #     values = {
        #         'header': 'Admission Closed!',
        #         'message': 'Admission Closed for Current Session!'
        #     }
        #     return request.render('odoocms_admission_portal.submission_message',values)

        # creating application for currently loged in user if application not already created

        academic_id = request.env['applicant.academic.detail'].sudo().search(
            [('application_id', '=', application_id.id)])
        degree_intermediate = request.env['odoocms.degree'].sudo().search([])
        # if not academic_id:
        #     academic_id = request.env['applicant.academic.detail'].sudo().create({
        #         'application_id': application_id.id
        #     })
        document_id = request.env['odoocms.application.documents'].sudo().search(
            [('application_id', '=', application_id.id)], limit=1)

        # pgc_institute_id = request.env['pgc.institute'].sudo().search([])
        # pgc_institute_applicant = request.env['applicant.pgc.scholarship'].sudo(
        # ).search([('application_id', '=', application_id.id)], limit=1)

        # merit_id = request.env['odoocms.merit.registers'].sudo().search(
        #     [('register_id', '=', application_id.register_id.id), ('publish_merit', '=', True)])
        # merit_student = request.env['odoocms.merit.register.line'].sudo().search(
        #     [('applicant_id.application_no', '=', current_user.login), ('merit_reg_id', 'in', merit_id.ids), ('selected', '=', True)])

        admit_card = request.env['applicant.entry.test'].sudo().search(
            [('student_id', "=", application_id.id)])

        context = {

            'steps_id': steps_id,
            'company': company,
            'descipline_id': descipline_id,
            'board_id': board_id,
            'center_id': center_id,
            'application_id': application_id,
            'undertaking': undertaking,
            'degree_intermediate': degree_intermediate,
            'profession_id': profession_id,
            'advertisement': advertisement,
            'last_institute_attend': False,
            'passing_year': passing_year,
            'document_id': document_id,
            'academic_id': academic_id,
            'academic_data': academic_data,
            'country_id': country_id,
            'province_id': province_id,
            'domicile_id': domicile_id,
            'city_id': city_id,
            'merit_student': False,
            'religion_id': religion_id,
            'pgc_institute_id': False,
            'admit_card': admit_card,
        }
        # 'pgc_institute_applicant': pgc_institute_applicant,
        # 'scholarship_need_base': scholarship_need_base,
        # 'need_base_scholarship': scholarship_need_base,
        return request.render('odoocms_admission_portal.admission_application', context)

    @route('/admission/application/save/', type='http', auth='user', method='POST', csrf=False)
    def save_application(self, **kw):
        try:
            if request.httprequest.method == 'POST':
                application = request.env['odoocms.application'].sudo().search(
                    [('application_no', '=', request.env.user.login)], limit=1)
                form_data = {}

                if kw.get('step_name') == 'personal':
                    # for persnol detail form

                    personal_detail = {
                        # 'last_school_attend': int(kw.get('last_institute_attend')) if kw.get('last_institute_attend', '').isnumeric() else '',
                        'advertisement': int(kw.get('advertisement')) if kw.get('advertisement', '').isnumeric() else '',
                        'first_name': kw.get('first_name') or '',
                        'middle_name': kw.get('middle_name') or '',
                        'last_name': kw.get('last_name') or '',
                        'gender': kw.get('gender') or '',
                        'date_of_birth': datetime.strptime(kw.get('date_of_birth'), '%m/%d/%Y') or '',
                        'blood_group': kw.get('blood_group') or '',
                        'father_name': kw.get('father_name') or '',
                        'father_cnic': int(kw.get('father_cnic').replace('-', '')) or '',
                        'father_status': kw.get('father_status') or '',
                        'mother_name': kw.get('mother_name') or '',
                        'mother_cnic': int(kw.get('mother_cnic').replace('-', '')) if (kw.get('mother_cnic').replace('-', '')).isnumeric() else '',
                        'sisters': kw.get('sisters') or '',
                        'brothers': kw.get('brothers') or '',
                        'mother_status': kw.get('mother_status') or '',
                        'disabled_person': kw.get('disabled_person') or '',
                        'disabled_person_detail': kw.get('disabled_person_detail') or '',
                        'first_in_family': kw.get('first_in_family') or '',
                        'first_in_family_detail': kw.get('first_in_family_detail') or '',
                        'disease': kw.get('disease_ddl') or '',
                        'disease_details': kw.get('disease_details') or '',
                        'sat_score': kw.get('sat_score') or '',
                        'religion_id': int(kw.get('religion_id')) if kw.get('religion_id') else False,
                        'nationality': int(kw.get('nationality')) if kw.get('nationality') else False,
                    }
                    if int(kw.get('nationality')) == 177:
                        personal_detail.update({
                            'cnic': int(kw.get('cnic').replace('-', '')) or '',
                            'province_id': int(kw.get('province_id')) if kw.get('province_id').isnumeric() else False,
                            'domicile_id': int(kw.get('domicile_id')) if kw.get('domicile_id').isnumeric() else False,

                        })
                    if int(kw.get('nationality')) != 177:
                        personal_detail.update({
                            'passport': kw.get('passport') or '',
                            'province2': kw.get('province2'),

                        })

                    # update family details
                    if personal_detail.get('father_status') == 'alive':
                        personal_detail.update({
                            'father_cell': int(kw.get('father_cell').replace('-', '')) if (kw.get('father_cell').replace('-', '')).isnumeric() else '',
                            'father_education': kw.get('father_education') or '',
                            'father_profession': kw.get('father_profession') or '',
                        })
                    if personal_detail.get('mother_status') == 'alive':
                        personal_detail.update({
                            'mother_cell': int(kw.get('mother_cell').replace('-', '')) if (kw.get('mother_cell').replace('-', '')).isnumeric() else '',
                            'mother_education': kw.get('mother_education') or '',
                            'mother_profession': kw.get('mother_profession') or '',
                        })

                    form_data.update(
                        {k: v for k, v in personal_detail.items() if v != '' and v != '0'})

                    application.write(form_data)
                    if application.step_no <= int(kw.get('step_no')):
                        application.step_no = int(application.step_no) + 1

                    return json.dumps({
                        'msg': 'Personal Details Updated',
                        'step_no': application.step_no,
                        'application_state': application.state,
                        'status': 'noerror',
                    })

                if kw.get('step_name') == 'contact':

                    contact_detail = {
                        'email': kw.get('email') or '',
                        'phone': kw.get('phone') or '',
                        'mobile': int(kw.get('mobile').replace('-', '')) if (kw.get('mobile').replace('-', '')).isnumeric() else '',
                        'street': kw.get('street') or '',
                        'street2': kw.get('street2') or '',
                        'city': kw.get('city') or '',
                        'zip': kw.get('zip') or '',
                    }
                    if kw.get('is_same_address') == 'on':
                        contact_detail.update({
                            'is_same_address': True,
                            'per_country_id': int(kw.get('per_country_id')) if kw.get('per_country_id').isnumeric() else '',
                            'per_street': kw.get('street') or '',
                            'per_street2': kw.get('street2') or '',
                            'per_city': kw.get('city') or '',
                            'per_zip': kw.get('zip') or '',
                        })
                    if kw.get('is_same_address') != 'on':
                        contact_detail.update({
                            'per_country_id': int(kw.get('per_country_id')) if kw.get('per_country_id').isnumeric() else '',
                            'per_street': kw.get('per_street') or '',
                            'per_street2': kw.get('per_street2') or '',
                            'per_city': kw.get('per_city') or '',
                            'per_zip': kw.get('per_zip') or '',
                        })
                    form_data.update(
                        {k: v for k, v in contact_detail.items() if v != ''})
                    application.write(form_data)
                    if application.step_no <= int(kw.get('step_no')):
                        application.step_no = int(application.step_no) + 1

                    return json.dumps({
                        'msg': f'Contact Details Updated',
                        'step_no': application.step_no,
                        'application_state': application.state,
                        'status': 'noerror',
                    })

                if kw.get('step_name') == 'guardian':
                    guardian_detail = {
                        'guardian_name': kw.get('guardian_name') or '',
                        'guardian_cell':  int(kw.get('guardian_cell').replace('-', '')) if (kw.get('guardian_cell', '').replace('-', '')).isnumeric() else '',
                        'guardian_cnic': int(kw.get('guardian_cnic').replace('-', '')) if kw.get('guardian_cnic').replace('-', '').isnumeric() else '',
                        'guardian_relation': kw.get('guardian_relation') or '',
                        'guardian_income': int(kw.get('guardian_income')) if kw.get('guardian_income', '').isnumeric() else '',
                        'guardian_address': kw.get('guardian_address') or '',
                        'guardian_education': kw.get('guardian_education') or '',
                        'guardian_profession': int(kw.get('guardian_profession')) if kw.get('guardian_profession', '').isnumeric() else '',
                        'fee_payer_name': kw.get('fee_payer_name', '') or False,
                        'fee_payer_cnic': kw.get('fee_payer_cnic', '') or False,
                    }

                    form_data.update(
                        {k: v for k, v in guardian_detail.items() if v != ''})
                    application.write(form_data)
                    if application.step_no <= int(kw.get('step_no')):
                        application.step_no = int(application.step_no) + 1

                    return json.dumps({
                        'msg': f'Guardian Details Updated',
                        'step_no': application.step_no,
                        'application_state': application.state,
                        'status': 'noerror',
                    })

                if kw.get('step_name') == 'education':
                    if application.applicant_academic_ids:
                        if int(kw.get('degree_level')) in [rec.degree_level_id.id for rec in application.applicant_academic_ids]:
                            return json.dumps({
                                'msg': f'Equivalent Degree Already Added',
                                'status': 'error'
                            })
                        # print(application.applicant_academic_ids.degree_level_id.id)

                    academic_data = {
                        'doc_state': 'no',
                        'degree_level_id': int(kw.get('degree_level')) if kw.get('degree_level').isnumeric() else '',
                        'degree_name': int(kw.get('degree')) if kw.get('degree').isnumeric() else '',
                        'group_specialization': int(kw.get('specialization')) if kw.get('specialization').isnumeric() else '',
                        'total_marks': int(kw.get('total_marks')) if kw.get('total_marks').isnumeric() else '',
                        'obt_marks': int(kw.get('obtained_marks')) if kw.get('obtained_marks').isnumeric() else '',
                        'percentage': kw.get('percentage') or '',
                        'roll_no': kw.get('roll_no') or '',
                        'application_id': application.id,
                        'board': kw.get('board') or '',
                        'institute': kw.get('institute') or '',
                    }
                    if kw.get('result_status'):
                        academic_data.update({
                            'result_status': kw.get('result_status') or ''
                        })


                    # if kw.get('degree_file') != 'undefined':
                    #     academic_data.update({
                    #         'attachment': base64.b64encode(kw.get('degree_file').read()) or ''
                    #     })

                    form_data.update(
                        {k: v for k, v in academic_data.items() if v != ''})
                    academic_add = application.applicant_academic_ids.create(
                        form_data)
                    application.write({'education_consent' : True})
                    if kw.get('subject_marks'):
                        subject_marks = json.loads(kw.get('subject_marks'))
                        if subject_marks != {}:
                            subject_marks_list = []
                            for k, v in subject_marks.items():
                                v = json.loads(v)
                                data_subject = {
                                    'name': int(k),
                                    'total_marks': int(v['subj_total_marks']),
                                    'obtained_marks': int(v['subj_marks']),
                                    'applicant_academic_id': academic_add.id,
                                }
                                academic_add.applicant_subject_id.create(
                                    data_subject)

                    context_academic_data = [{
                        'id': rec.id,
                        'percentage': rec.percentage or '',
                        'degree_name': rec.degree_name.name or '',
                        'specialization': rec.group_specialization.name or '',
                        'degree_level': rec.degree_level_id.name or None,
                        'state': rec.result_status,
                        'institue': rec.institute or None,
                    } for rec in application.applicant_academic_ids]

                    education_criteria = 'no'
                    applicant_education_year = max(
                        [int(year.year_age) for year in application.applicant_academic_ids.degree_name])

                    if applicant_education_year >= application.register_id.min_edu_year or 0:
                        if application.step_no <= int(kw.get('step_no')):
                            application.step_no = int(application.step_no) + 1
                        education_criteria = 'yes'

                    return json.dumps({
                        'education_criteria': education_criteria,
                        'academic_data': context_academic_data,
                        'msg': f'Education Details Updated',
                        'step_no': application.step_no,
                        'application_state': application.state,
                        'status': 'noerror'
                    })

                    if not application.academic_ids:
                        if application.step_no <= int(kw.get('step_no')):
                            application.step_no = int(application.step_no) + 1
                    if application.academic_ids:
                        for rec in application.academic_ids:
                            if rec.degree_level_year == kw.get('degree_level_year'):
                                return json.dumps({
                                    'msg': f'Equivalent Degree Already Added',
                                    'status': 'error'
                                })

                if kw.get('step_name') == 'document':

                    cnic_file = kw.get('cnic_file')
                    cnic_back_file = kw.get('cnic_back_file')
                    domicile_file = kw.get('domicile_file')
                    passport_file = kw.get('passport')

                    document_data = {}

                    if application.applicant_type == 'national':
                        if type(cnic_file) == FileStorage:
                            document_data.update({
                                'cnic_front': base64.b64encode(cnic_file.read()) or '',
                            })
                        if type(cnic_back_file) == FileStorage:
                            document_data.update({
                                'cnic_back': base64.b64encode(cnic_back_file.read()) or '',
                            })
                        if type(domicile_file) == FileStorage:
                            document_data.update({
                                'domicile': base64.b64encode(domicile_file.read()) or '',
                            })
                    if application.applicant_type == 'international':
                        if type(passport_file) == FileStorage:
                            document_data.update({
                                'pass_port': base64.b64encode(passport_file.read()) or '',
                            })

                    form_data.update(
                        {k: v for k, v in document_data.items() if v != ''})

                    application.sudo().write(form_data)
                    if application.step_no <= int(kw.get('step_no')):
                        application.step_no = int(application.step_no) + 1

                    return json.dumps({
                        'msg': 'Documents Details Updated',
                        'step_no': application.step_no,
                        'application_state': application.state,
                        'status': 'noerror',
                    })

                if kw.get('step_name') == 'fee_voucher':
                    if kw.get('step_skip') and kw.get('step_skip') == 'yes':
                        if application.step_no <= int(kw.get('step_no')):
                            application.step_no = int(application.step_no) + 1
                        return json.dumps({
                            'msg': 'Fee Voucher Details Updated',
                            'step_no': application.step_no,
                            'application_state': application.state,
                            'status': 'noerror',
                        })

                    # 'fee_voucher_state': 'upload',
                    voucher_image = kw.get('voucher_image')
                    voucher_data = {
                        'fee_voucher_state': kw.get('upload0'),
                        'voucher_number': kw.get('voucher_number') or '',
                        'voucher_date': datetime.strptime(kw.get('voucher_date'), '%Y-%m-%d') or '',
                    }
                    if voucher_image != 'undefined':
                        voucher_data.update({
                            'voucher_image': base64.b64encode(voucher_image.read()) or '',
                        })
                    form_data.update(
                        {k: v for k, v in voucher_data.items() if v != ''})
                    application.write(form_data)
                    if application.step_no <= int(kw.get('step_no')):
                        application.step_no = int(application.step_no) + 1

                    return json.dumps({
                        'msg': 'Fee Voucher Details Updated',
                        'step_no': application.step_no,
                        'application_state': application.state,
                        'status': 'noerror',
                    })

                if kw.get('step_name') == 'program_transfer':
                    try:
                        if not kw.get('new_selected_program'):
                            if application.step_no <= int(kw.get('step_no')):
                                application.step_no = int(
                                    application.step_no) + 1
                                return json.dumps({
                                    'msg': 'Skiped!',
                                    'step_no': application.step_no,
                                    'application_state': application.state,
                                    'status': 'noerror',
                                })

                        pending_request = request.env['odoocms.program.transfer.request'].sudo().search(
                            [('applicant_id', '=', application.id)])
                        if not pending_request:
                            program_transfer_request = request.env['odoocms.program.transfer.request'].sudo().create({
                                'applicant_id': application.id,
                                'current_program': int(kw.get('new_selected_program')),
                                'previous_program': int(kw.get('current_program')),
                            })
                        if pending_request:
                            if pending_request.state == 'draft':
                                program_transfer_request = request.env['odoocms.program.transfer.request'].sudo().create({
                                    'applicant_id': application.id,
                                    'current_program': int(kw.get('new_selected_program')),
                                    'previous_program': int(kw.get('current_program')),
                                })
                                pending_request.unlink()
                        if application.step_no <= int(kw.get('step_no')):
                            application.step_no = int(application.step_no) + 1
                        return json.dumps({
                            'msg': 'Program Trasferred Request Created!',
                            'step_no': application.step_no,
                            'application_state': application.state,
                            'status': 'noerror',
                        })

                    except Exception as e:
                        return json.dumps({
                            'msg': f'{e}',
                            'step_no': application.step_no,
                            'application_state': application.state,
                            'status': 'error',
                        })

                if kw.get('step_name') == 'preference':

                    if application.preference_ids:
                        application.preference_ids.unlink()
                    data_kw = kw.copy()
                    data_kw.pop('pre_test_marks')
                    data_kw.pop('step_name')
                    data_kw.pop('step_no')
                    for k, v in data_kw.items():
                        preference = request.env['odoocms.application.preference'].sudo().create({
                            'preference': int(k),
                            'program_id': int(v),
                            'application_id': application.id,
                        })

                    if kw.get('pre_test_marks') != '':

                        application.pre_test_marks = int(
                            kw.get('pre_test_marks'))
                        application.pre_test_id = preference.filtered(
                            lambda x: x.preference == 1).program_id.pre_test.id
                    # if not application.prospectus_inv_id:
                    #     application.action_create_prospectus_invoice()
                    if application.step_no <= int(kw.get('step_no')):
                        application.step_no = int(application.step_no) + 1

                    return json.dumps({
                        'msg': 'Preferences Details Updated',
                        'step_no': application.step_no,
                        'application_state': application.state,
                        'status': 'noerror',
                    })

                if kw.get('step_name') == 'scholarship':
                    need_base = {
                        'guardian_occupation': kw.get('guardian_occupation_scho') or '',
                        'guardian_monthly_income': kw.get('guardian_monthly_income') or '',
                        'family_member': kw.get('family_member_scho') or '',
                        'guardian_job_status': kw.get('job_status_scho') or '',
                        'residential_status': kw.get('residential_status') or '',
                    }

                    pgc = {
                        'previous_school_attend': kw.get('previous_school_attend_scho') or '',
                        'pgc_registration_no': kw.get('pgc_registration_number_scho') or '',
                    }
                    if kw.get('pgc_institute'):
                        pgc.update({
                            'pgc_institute_id': int(kw.get('pgc_institute')) or '',

                        })

                    form_data.update(
                        {k: v for k, v in need_base.items() if v != '' and v != '0'})
                    form_data.update(
                        {k: v for k, v in pgc.items() if v != '' and v != '0'})

                    application.write(form_data)

                    if application.step_no <= int(kw.get('step_no')):
                        application.step_no = int(application.step_no) + 1

                    return json.dumps({
                        'msg': f'Scholarship Details Updated',
                        'step_no': application.step_no,
                        'application_state': application.state,
                        'status': 'noerror',
                    })

        except Exception as e:
            return json.dumps({
                'msg': f'Error! {e}',
                'status': 'error',
                'step_no': application.step_no,
                'application_state': application.state,
            })

    @route('/test/slot/', type='http', auth='user', method='POST', csrf=False)
    def test_slot(self, **kw):
        '''return the slot of test centere if available'''
        try:
            center_id = int(kw.get('test_center_id'))
            center_slot = request.env['odoocms.admission.test.center'].sudo().search(
                [('id', '=', center_id)]).time_ids.filtered(lambda x: x.active_time)
            slot_data = []
            for slot in center_slot:
                slot_data.append(
                    {'id': slot.id, 'name': str(slot.date) if slot.date else '' + ' ' + str(slot.time) if slot.time else ''})

            record = {
                'status': "noerror",
                'slots_data': slot_data}

            return json.dumps(record)
        except Exception as e:
            return json.dumps({
                'Error': '%s' % e
            })

    @route('/province/domicile/', type='http', auth='user', method='POST', csrf=False)
    def province_domicile(self, **kw):
        """
        This Function is used for geting the domiciles of specific province(given through ajax request)

        Returns:
            list-of-dict: status and list of domiciles
        """
        try:
            province_id = int(kw.get('province_id'))

            domiciles = request.env['odoocms.domicile'].sudo().search(
                [('province_id', '=', province_id)])
            domicile_data = []
            for domicile in domiciles:
                domicile_data.append(
                    {'id': domicile.id, 'name': domicile.name})
            record = {
                'status_is': "noerror",
                'domiciles': domicile_data, }
            return json.dumps(record)
        except Exception as e:
            return json.dumps({
                'Error': '%s' % e
            })

    @route('/degree/level/degree/', type='http', auth='user', method='POST', csrf=False)
    def degree_level_degree(self, **kw):
        """

        """
        try:
            degree_id = int(kw.get('degree_id'))

            degrees = request.env['odoocms.admission.education'].sudo().search(
                [('id', '=', degree_id)]).degree_ids
            degree_data = []
            for degree in degrees:
                degree_data.append(
                    {'id': degree.id, 'name': degree.name})
            record = {
                'status': "noerror",
                'degrees': degree_data, }
            return json.dumps(record)
        except Exception as e:
            return json.dumps({
                'status': 'error',
                'Error': '%s' % e
            })

    @route('/degree/specializations/', type='http', auth='user', method='POST', csrf=False)
    def degree_specializations(self, **kw):

        try:
            degree_id = int(kw.get('degree_id'))

            specilizations = request.env['odoocms.admission.degree'].sudo().search(
                [('id', '=', degree_id)]).specialization_ids
            specialization_data = []
            for specilization in specilizations:
                specialization_data.append(
                    {'id': specilization.id, 'name': specilization.name})
            record = {
                'status': "noerror",
                'specializations': specialization_data, }
            return json.dumps(record)
        except Exception as e:
            return json.dumps({
                'status': 'error',
                'Error': '%s' % e
            })

    @route('/degree/specializations/subjects/', type='http', auth='user', method='POST', csrf=False)
    def degree_specializations_subject(self, **kw):

        try:
            specialization_id = int(kw.get('specialization_id'))
            specilizations_subject = request.env['applicant.academic.group'].sudo().search(
                [('id', '=', specialization_id)]).academic_subject_ids
            specialization_subject_data = []
            for subject in specilizations_subject:
                specialization_subject_data.append(
                    {'id': subject.id, 'name': subject.name})
            record = {
                'status': "noerror",
                'specializations_subject': specialization_subject_data, }
            return json.dumps(record)
        except Exception as e:
            return json.dumps({
                'status': 'error',
                'Error': '%s' % e,
            })

    @route('/descipline/program/', type='http', auth='user', method='POST', csrf=False)
    def descipline_program(self, **kw):
        try:
            descipline_code = kw.get('descipline_id')
            programs = request.env['odoocms.discipline'].sudo().search(
                [('code', '=', descipline_code), ]).program_ids
            program_data = []
            for program in programs:
                program_data.append({
                    'code': program.code,
                    'program': program.name,
                })
            record = {
                'status_is': 'noerror',
                'program': program_data,
            }
            return json.dumps(record)
        except Exception as e:
            return json.dumps({
                'Error': '%s' % e
            })

    @route('/education/update/', type='http', auth='user', method='POST', csrf=False)
    def update_education(self, **kw):
        try:
            academic_education = {k: v for k, v in kw.items() if v != ''}
            academic_education['application_id'] = int(
                kw.get('application_id'))
            request.env['applicant.academic.detail'].sudo().create(
                academic_education)
            return json.dumps({
                'is_success': 'yes'
            })
        except Exception as e:
            return json.dumps({
                'is_success': 'no',
                'exception': f'Error! {e}'
            })

    @route('/profile/image/update/', type='http', auth='user', method='POST', csrf=False)
    def profile_image_update(self, **kw):
        try:
            application = request.env['odoocms.application'].sudo().search(
                [('application_no', '=', request.env.user.login)], limit=1)
            if request.httprequest.method == 'POST':
                image = kw.get('image_file')
                application.write({
                    'image': base64.b64encode(image.read()),
                })
                return json.dumps({
                    'msg': f'Profle Picture Updated!!',
                    'status': 'noerror',
                })
        except Exception as e:
            return json.dumps({
                'msg': f'Error!',
                'status': 'error',
                'step_no': application.step_no,
                'application_state': application.state,
            })

    @route('/download/admission/slip/', csrf=False, type="http", methods=['POST', 'GET'], auth="public", website=True)
    def download_admission_slip(self, **kw):
        current_user = request.env.user

        application = request.env['odoocms.application'].sudo().search(
            [('application_no', '=', current_user.login)])

        application.sudo().write({
            'fee_voucher_state': 'download'
        })
        application.fee_voucher_download_date = date.today()
        pdf_report = request.env.ref('odoocms_admission_portal.action_report_admission_invoices').sudo(
        )._render_qweb_pdf([application.id])[0]
        pdfhttpheaders = [('Content-Type', 'application/pdf'),
                          ('Content-Length', len(pdf_report))]
        return request.make_response(pdf_report, headers=pdfhttpheaders)

    @route('/download/fee/invoice/', csrf=False, type="http", methods=['POST', 'GET'], auth="public", website=True)
    def download_fee_invoice(self, **kw):
        current_user = request.env.user

        application = request.env['odoocms.application'].sudo().search(
            [('application_no', '=', current_user.login)])

        fee_invoice = request.env['account.move'].sudo().search(
            [('application_id', '=', application.id)], limit=1)
        if fee_invoice:
            pdf_report = request.env.ref('odoocms_fee.action_report_student_invoice_landscape').sudo(
            )._render_qweb_pdf([fee_invoice.id])[0]
            pdfhttpheaders = [('Content-Type', 'application/pdf'),
                              ('Content-Length', len(pdf_report))]
            return request.make_response(pdf_report, headers=pdfhttpheaders)

    @route('/apply/application/', csrf=False, type="http", methods=['GET'], auth="user")
    def apply_application(self, **kw):
        current_user = request.env.user
        application = request.env['odoocms.application'].sudo().search(
            [('application_no', '=', current_user.login)])
        # if not application.prospectus_inv_id:
        #     application.action_create_prospectus_invoice()
        if application.state == 'draft':
            application.state = 'submit'
            # if application.step_no <= int(kw.get('step_no')):
            application.step_no = int(application.step_no) + 1
            return json.dumps({
                'msg': f'Application Submitted!',
                'application_state': application.state,
                'step_no': application.step_no,
                'application_state': application.state,
                'status': 'noerror',

            })
        else:
            return json.dumps({
                'msg': f'Application Already Submitted!',
                'status': 'error',
                'step_no': application.step_no,
                'application_state': application.state,

            })

    @route('/delete/education/', csrf=False, type="http", methods=['POST', 'GET'], auth="user")
    def delete_education(self, **kw):
        current_user = request.env.user
        application_id = request.env['odoocms.application'].sudo().search(
            [('application_no', '=', current_user.login)], limit=1)
        edu_id = kw.get('edu_id')
        application_id.applicant_academic_ids.sudo().search(
            [('id', '=', edu_id)]).unlink()
        return json.dumps({
            'msg': f'Education Removed!',

        })

    @route('/prepare/admission/invoice/', csrf=False, type="http", methods=['GET'], auth="user")
    def prepare_admission_invoice(self, **kw):
        current_user = request.env.user
        application_id = request.env['odoocms.application'].sudo().search(
            [('application_no', '=', current_user.login)])

        disciplines = 0
        discipline = 0
        prefs = request.env['odoocms.application.preference'].sudo().search(
            [('application_id', '=', application_id.id)])

        first_preference = prefs.filtered(lambda x: x.preference == 1)
        seat_avail_program = first_preference.program_id
        for program in seat_avail_program:
            print(seat_avail_program)
            if program.signin_end_date:
                if program.signin_end_date <= date.today():
                    data = json.dumps({
                        'error': 'unavailable',
                    })

                    return data

        program_preferences_ordered = http.request.env['odoocms.application.preference'].sudo().search(
            [('application_id', '=', application_id.id)], order='preference asc')
        selected_discipline = []
        for program in program_preferences_ordered:
            selected_discipline += str(program.discipline_id.id)
        selected_discipline = list(dict.fromkeys(selected_discipline))
        for i in range(0, len(selected_discipline)):
            selected_discipline[i] = (selected_discipline[i])
        for pref in prefs:
            if pref.discipline_id.id != discipline:
                discipline = pref.discipline_id.id
                disciplines = disciplines + 1

        registration_fee_international = http.request.env['ir.config_parameter'].sudo(
        ).get_param('odoocms_admission_portal.registration_fee_international')
        registration_fee = http.request.env['ir.config_parameter'].sudo(
        ).get_param('odoocms_admission_portal.registration_fee')
        additional_fee = http.request.env['ir.config_parameter'].sudo(
        ).get_param('odoocms_admission_portal.additional_fee')

        account_payable = http.request.env['ir.config_parameter'].sudo(
        ).get_param('odoocms_admission_portal.account_payable')
        account_title = http.request.env['ir.config_parameter'].sudo(
        ).get_param('odoocms_admission_portal.account_title')
        account_no = http.request.env['ir.config_parameter'].sudo(
        ).get_param('odoocms_admission_portal.account_no')

        account_payable2 = http.request.env['ir.config_parameter'].sudo(
        ).get_param('odoocms_admission_portal.account_payable2')
        account_title2 = http.request.env['ir.config_parameter'].sudo(
        ).get_param('odoocms_admission_portal.account_title2')
        account_no2 = http.request.env['ir.config_parameter'].sudo(
        ).get_param('odoocms_admission_portal.account_no2')

        total_fee = 0
        # for rec in selected_discipline:
        if application_id.degree.code == 'DAECIVIL':
            choices = program_preferences_ordered.filtered(
                lambda l: l.discipline_id.code == 'TECH' or l.discipline_id.code == 'E')
            for ch in choices:
                if total_fee < 4000:
                    total_fee += int(float(registration_fee))
        else:
            total_fee = int(float(registration_fee))
        # if disciplines > 1:
        #     total_fee += int(float(additional_fee))

        docargs = {
            'is_dual_nationality': application_id.is_dual_nationality or application_id.overseas or application_id.nationality.id != 177,
            'student_name': application_id.first_name + ' ' + application_id.last_name,
            'father_name': application_id.father_name,
            'cnic': application_id.cnic,
            'account_payable': account_payable or "",
            'account_payable2': account_payable2 or "",
            'registration_fee': registration_fee or False,
            'additional_fee': additional_fee or False,
            'fee_voucher_state': application_id.fee_voucher_state or False,
            'total_fee': str(total_fee),
            'total_fee_word': application_id.amount_to_text(float(total_fee)),
            'registration_fee_international': registration_fee_international or False,
            'total_fee_word_international': application_id.amount_to_text(float(registration_fee_international)),
            'account_title': account_title or " ",
            'account_title2': account_title2 or " ",
            'account_no': account_no or "",
            'account_no2': account_no2 or "",
            'disciplines': disciplines,
            'today': date.today().strftime('%Y/%d/%m') or False,
        }
        if application_id.fee_voucher_state in ('no', 'download'):
            application_id.fee_voucher_state = 'download'
        docargs.update({'fee_voucher_state': 'download'})

        data = json.dumps(docargs)
        return data

    @route('/prepare/preference/', csrf=False, type="http", methods=['GET'], auth="user")
    def prepare_preference(self, **kw):
        try:
            application = request.env['odoocms.application'].sudo().search(
                [('application_no', '=', request.env.user.login)], limit=1)
            academic_info = application.applicant_academic_ids
            applicant_academic_degree = [
                rec.degree_name.id for rec in academic_info if rec.degree_name]
            academic_specialization = [
                rec.group_specialization.id for rec in academic_info if rec.group_specialization]
            offered_prgram = request.env['odoocms.degree'].sudo().search(
                [('degree_id', 'in', applicant_academic_degree), ('specialization_id', 'in', academic_specialization)])
            offered_program_eligible = offered_prgram.filtered(lambda x: x.eligibilty_percentage <= academic_info.search([
                                                               ('degree_name', '=', x.degree_id.id), ('application_id', '=', application.id)]).percentage)
            context = {}
            pre_test_context = {}

            # pretest_checked_id = preference_selected.filtered(
            #         lambda x: x.preference == 1).program_id.id
            #     pretest_check_program = request.env['odoocms.program'].sudo().search(
            #         [('id', '=', pretest_checked_id)])
            #     if pretest_check_program.pre_test:
            #         return json.dumps({
            #             'pre_test': pretest_check_program.pre_test.id,
            #             'pre_test_name': pretest_check_program.pre_test.name,
            #             'status': 'pretest'
            #         })
            for rec in offered_program_eligible:
                for program in rec.program_ids:
                    if program.id and program.offering:
                        if program.signup_end_date:
                            if program.signup_end_date >= date.today():
                                if program.signin_end_date:
                                    if program.signin_end_date <= date.today():
                                        context.update({
                                            program.id: program.name
                                        })
                                        pre_test_context.update({
                                            program.id: {
                                                program.pre_test.id: program.pre_test.name} if program.pre_test else False
                                        })
                                    if not program.signin_end_date:
                                        context.update({
                                            program.id: program.name
                                        })

                                        pre_test_context.update({
                                            program.id: {
                                                program.pre_test.id: program.pre_test.name} if program.pre_test else False
                                        })

                        if not program.signup_end_date:
                            if program.signin_end_date:
                                if program.signin_end_date <= date.today():
                                    context.update({
                                        program.id: program.name
                                    })
                                    pre_test_context.update({
                                        program.id: {
                                            program.pre_test.id: program.pre_test.name} if program.pre_test else False
                                    })
                            if not program.signin_end_date:
                                context.update({
                                    program.id: program.name
                                })
                                pre_test_context.update({
                                    program.id: {
                                        program.pre_test.id: program.pre_test.name} if program.pre_test else False
                                })

            return json.dumps({
                'pretest': pre_test_context,
                'program_offered': context,
                'status': 'noerror'
            })
        except Exception as e:
            return json.dumps({
                'status': 'error',
                'error': f'{e}'
            })

    @route('/download/admit/', csrf=False, type="http", methods=['GET'], auth="user")
    def download_admit_card(self, **kw):
        report_type = "pdf"

        application = request.env['odoocms.application'].sudo().search(
            [('application_no', '=', request.env.user.login)], limit=1)
        admit_card = request.env['applicant.entry.test'].sudo().search(
            [('student_id', "=", application.id)])
        # if not admit_card.slot_type:
        #     report_ref=
        if admit_card.slot_type == 'test' or not admit_card.slot_type:
            report_ref = 'odoocms_admission_nutech.action_student_admit_card'
        if admit_card.slot_type == 'interviewer':
            report_ref = 'odoocms_admission_nutech.action_student_interview_admit_card'

        # report_ref = 'odoocms_admission_portal.action_student_admit_card_download'
        return self._show_report_admit(model=admit_card, report_type=report_type, report_ref=report_ref, download="download")

    @route('/download/admit/<test>', csrf=False, type="http", methods=['GET'], auth="user")
    def download_admit_card_suffa(self, **kw):

        report_type = "pdf"

        application = request.env['odoocms.application'].sudo().search(
            [('application_no', '=', request.env.user.login)], limit=1)
        admit_card = request.env['applicant.entry.test'].sudo().search(
            [('student_id', "=", application.id)])
        # if not admit_card.slot_type:
        #     report_ref=
        if kw.get('test') == 'test':
            report_ref = 'odoocms_admission_nutech.action_student_admit_card'
        if kw.get('test') == 'interview':
            report_ref = 'odoocms_admission_nutech.action_student_interview_admit_card'

        # report_ref = 'odoocms_admission_portal.action_student_admit_card_download'
        return self._show_report_admit(model=admit_card, report_type=report_type, report_ref=report_ref, download="download")

    @route('/get/merit/', csrf=False, type="http", methods=['GET'], auth="user")
    def get_merit(self, **kw):
        try:
            application = request.env['odoocms.application'].sudo().search(
                [('application_no', '=', request.env.user.login)], limit=1)
            merit_current_user = request.env['odoocms.merit.register.line'].sudo().search(
                [('applicant_id', '=', application.id)])
            return json.dumps({
                'status': 'noerror',
                'merit_no': merit_current_user.merit_no,
                'score': merit_current_user.score,
                'aggregate': merit_current_user.aggregate,
            })
        except Exception as e:
            return json.dumps({
                'error': f'{e}',
                'status': 'noerror',
            })

    @http.route(['/file/download/<int:id>/<model>'], type='http', auth="user", website=True, csrf=False)
    def download_attachment_file(self, model=None, id=0, **kw):

        env = http.request.env
        record = env[str(model)].sudo().browse(int(id))

        status, content, filename, mimetype, filehash = env['ir.http'].sudo(
        )._binary_record_content(record, field=str('attachment'))
        status, headers, content = env['ir.http'].sudo()._binary_set_headers(status, content, filename, mimetype,
                                                                             unique=False, filehash=filehash,
                                                                             download=True)
        if status != 200:
            return request.env['ir.http'].sudo()._response_by_status(status, headers, content)
        else:
            content_base64 = base64.b64decode(content)
            headers.append(('Content-Length', len(content_base64)))
            response = request.make_response(content_base64, headers)
        return response

    # download invoice nutech
    @route('/download/invoice/admission/', csrf=False, type="http", methods=['POST', 'GET'], auth="public", website=True)
    def download_inovoice_slip(self, **kw):
        current_user = request.env.user

        application = request.env['odoocms.application'].sudo().search(
            [('application_no', '=', current_user.login)])

        if application.fee_voucher_state =='no':
            application.fee_voucher_state = 'download'
            application.fee_voucher_download_date = date.today()
            application.voucher_issued_date = date.today()

        invoice_id = application.prospectus_inv_id
        pdf_report = request.env.ref('odoocms_fee_ext.action_report_term_fee_challan').sudo(
        )._render_qweb_pdf([invoice_id.id])[0]
        pdfhttpheaders = [('Content-Type', 'application/pdf'),
                          ('Content-Length', len(pdf_report))]
        return request.make_response(pdf_report, headers=pdfhttpheaders)

    @http.route('/download/admission/feevoucher', csrf=False, type="http", methods=['POST', 'GET'], auth="public",
                website=True)
    def download_admission_fee_voucher(self, **kw):
        current_user = http.request.env.user

        register = http.request.env['odoocms.admission.register'].sudo().search(
            [('state', '=', 'application')])
        application = http.request.env['odoocms.application'].sudo().search(
            [('cnic', '=', current_user.login), ('register_id', '=', register.id)])
        return application._show_report(model=application, report_type='pdf',
                                        report_ref='odoocms_admission_portal.student_admission_invoice', download=True)

    # download invoice nutech
    @route('/download/offer/letter/', csrf=False, type="http", methods=['POST', 'GET'], auth="user", website=True)
    def download_offer_letter(self, **kw):
        # current_user = request.env.user
        # application = request.env['odoocms.application'].sudo().search(
        #     [('application_no', '=', current_user.login)])
        # pdf_report = request.env.ref('odoocms_admission_nutech.admission_offer_letter').sudo(
        # )._render_qweb_pdf([offer_letter.id])[0]
        # pdfhttpheaders = [('Content-Type', 'application/pdf'),
        #                   ('Content-Length', len(pdf_report))]
        # return request.make_response(pdf_report, headers=pdfhttpheaders)
        report_type = "pdf"

        application = request.env['odoocms.application'].sudo().search(
            [('application_no', '=', request.env.user.login)], limit=1)
        
        offer_letter = request.env['admission.offer.letter'].sudo().search(
            [('applicant_id', '=', application.id)],limit=1)
        
        report_ref = 'odoocms_admission_nutech.admission_offer_letter'
        # if not admit_card.slot_type:
        # #     report_ref=
        # if kw.get('test') == 'test':
        # if kw.get('test') == 'interview':
        #     report_ref = 'odoocms_admission_nutech.action_student_interview_admit_card'

        # report_ref = 'odoocms_admission_portal.action_student_admit_card_download'
        return self._show_report_admit(model=offer_letter, report_type=report_type, report_ref=report_ref, download="download")
