from odoo.http import route, request, Controller
import json


class DashboardStudentAdmission (Controller):
    @route(['/admission/student/dashboard'], method='GET', type='http', auth="user")
    def admission_student_dashboard(self, **kw):
        company = request.env.company
        user = request.env.user
        application_id = request.env['odoocms.application'].sudo().search(
            [('application_no', '=', user.login)])
        admit_card = request.env['applicant.entry.test'].sudo().search(
            [('student_id', "=", application_id.id)])

        merit_id = request.env['odoocms.merit.registers'].sudo().search(
            [('register_id', '=', application_id.register_id.id), ('publish_merit', '=', True)])
        merit_student = request.env['odoocms.merit.register.line'].sudo().search(
            [('applicant_id.application_no', '=', user.login), ('merit_reg_id', 'in', merit_id.ids), ('selected', '=', True)])
        pending_request = request.env['odoocms.program.transfer.request'].sudo().search(
            [('applicant_id', '=', application_id.id), ('state', '=', 'draft')])

        fee_invoice = request.env['account.move'].sudo().search(
            [('application_id', '=', application_id.id)])

        context = {
            'fee_invoice': fee_invoice,
            'company': company,
            'merit_student': merit_student,
            'pending_request': pending_request,
            'admit_card': admit_card,
            'user': user,
            'application_id': application_id,
        }
        return request.render('odoocms_admission_portal.admission_student_dashboard', context)

    @route(['/program/transfer/'], method='GET', csrf=False, type='http', auth="user")
    def program_transfer_request(self, **kw):
        try:
            
            application_id = request.env['odoocms.application'].sudo().search(
                [('application_no', '=', request.env.user.login)])

            # if kw.get('pre_test_marks', False):
            #     application_id.pre_test_marks = int(kw.get('pre_test_marks'))
            program_transfer_from = kw.get('program_transfer_from')
            program_transfer_to = kw.get('program_transfer_to')

            pending_request = request.env['odoocms.program.transfer.request'].sudo().search(
                [('applicant_id', '=', application_id.id)])
            if not pending_request:
                program_transfer_request = request.env['odoocms.program.transfer.request'].sudo().create({
                    'applicant_id': application_id.id,
                    'current_program': program_transfer_to,
                    'previous_program': program_transfer_from,
                    'pre_test_marks':kw.get('pre_test_marks'),
                })
            if pending_request:
                if pending_request.state == 'draft':
                    pending_request.unlink()
                    program_transfer_request = request.env['odoocms.program.transfer.request'].sudo().create({
                        'applicant_id': application_id.id,
                        'pre_test_marks':kw.get('pre_test_marks'),
                        'current_program': program_transfer_from,
                        'previous_program': program_transfer_to,
                    })

            return json.dumps({
                'status': 'noerror',
            })

        except Exception as e:
            return json.dumps({
                'msg': f'{e}',
                'application_state': application_id.state,
                'status': 'error',
            })
