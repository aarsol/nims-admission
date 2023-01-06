from odoo import http
import random
import string
from odoo.http import route, request, Controller
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.exceptions import UserError
import logging
from odoo import _
from odoo.service import db, security
import odoo
import werkzeug
import odoo.addons.web.controllers.main as main
from odoo.addons.auth_signup.models.res_users import SignupError
_logger = logging.getLogger(__name__)


class AccountRegistration(Controller):

    @route(['/web/signin/'], method='GET', type='http', auth="public", sitemap=False)
    # def index_signin(self, redirect=None, **kw):
    #
    #     career_id = request.env['odoocms.admission.register'].sudo().search(
    #         [('state', '=', 'application')]).career_id
    #     country_id = request.env['res.country'].sudo().search([])
    #
    #     values = {
    #         'country_id': country_id,
    #         'career_id': career_id,
    #         'company': request.env.company
    #     }
    #     if kw.get('signup') == 'True':
    #         request.session.logout(keep_db=True)
    #         # db_select = '/web/signin?db=%s' % request._cr.dbname
    #         # return http.local_redirect(db_select)
    #         values.update({
    #             'message': 'Login Details Send By Email!'
    #         })
    #         return request.render('odoocms_admission_portal.account_registration', values)
    #     request.session.logout(keep_db=True)
    #     return request.render('odoocms_admission_portal.account_registration', values)

    def index_signin(self, redirect=None, **kw):
        career_id = request.env['odoocms.admission.register'].sudo().search(
            [('state', '=', 'application')]).career_id

        country_id = request.env['res.country'].sudo().search([])

        values = {
            'country_id': country_id,
            'career_id': career_id,
            'company': request.env.company
        }
        return request.render('odoocms_admission_portal.account_registration', values)


class AdmissionSignUp(Home):

    @http.route('/web/admission/signup/', type='http', csrf=False, auth='public', website=True, sitemap=False)
    def web_auth_admission_signup(self, *args, **kw):

        qcontext = self.get_auth_signup_qcontext()
        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()
        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                career_id = request.env['odoocms.admission.register'].sudo().search(
                    [('state', '=', 'application')]).career_id
                country_id = request.env['res.country'].sudo().search([])
                qcontext.update({
                    'country_id': country_id,
                    'career_id': career_id,
                    'company': request.env.company
                })

                country = int(kw.get('country_id_signup')) if kw.get(
                    'country_id_signup', '').isnumeric() else 177

                check_email = request.env['res.users'].sudo().search(
                    [('email', '=', kw.get('email'))])
                if check_email:
                    raise UserError('Email Already Registerd Please Signin')
                career_id = int(kw.get('career_id'))
                international_student = kw.get('international_student')
                admission_register = request.env['odoocms.admission.register'].sudo().search(
                    [('state', '=', 'application'), ('career_id', '=', career_id)])
                cnic = False
                if kw.get('cnic') != '':
                    cnic = int(kw.get('cnic').replace(
                        '-', '')) if (kw.get('cnic').replace('-', '')).isnumeric() else False,
                length = 8
                all = string.ascii_letters + string.digits + '$#'

                password = "".join(random.sample(all, length))
                application = admission_register.application_ids.create({
                    'register_id': admission_register.id,
                    'mobile': kw.get('phone'),
                    'applicant_type': international_student,
                    'nationality': country,
                    'email': kw.get('email'),
                    'first_name': kw.get('first_name'),
                    'last_name': kw.get('last_name'),
                    'step_no': 1,
                    'gender': kw.get('gender'),
                    'cnic': cnic,
                    'password': password
                })


                qcontext.update({
                    'login': application.application_no,
                    'name': kw.get('first_name') + ' ' + kw.get('last_name'),
                    'password': password,
                    'phone': kw.get('phone'),
                    'country_id': country,
                    'confirm_password': password,
                })
                kw.update(qcontext)

                self.admission_signup(qcontext)
                application.user_id = request.env['res.users'].sudo().search(
                    [('login', '=', application.application_no)]).id

                template = request.env.ref(
                    'odoocms_admission.mail_template_account_created').sudo()

                login_value = {
                    'company_name': request.env.company.name or "",
                    'company_website': request.env.company.website or "",
                    'company_email': request.env.company.admission_mail or "",
                    'company_phone': request.env.company.admission_phone or "",
                    'login': application.application_no, 'password': password}
                user = request.env['res.users'].sudo().search(
                    [('login', '=', application.application_no)])
                template.with_context(login_value).send_mail(
                    user.id, force_send=True)
                # return http.local_redirect('/web/signin/', {'signup': True})
                # application.message_post_with_template(template.with_context(password_values).id)

                # user_sudo = request.env['res.users'].sudo().search([('login', '=', qcontext.get('login'))])
                # template = request.env.ref('odoocms_graduate_admission.mail_template_user_signup_account_created', raise_if_not_found=False)
                # if user_sudo:
                #     template.sudo().with_context(lang=user_sudo.lang, auth_login=werkzeug.url_encode({'auth_login': user_sudo.email}),).send_mail(user_sudo.id, force_send=True)
                # raise UserError('Login Details Send To Your Mail')
                return self.web_login_admission(*args, **kw)

            except UserError as e:
                qcontext['error'] = e.name or e.value
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _(
                        "Another user is already registered using this email address.")
                else:
                    _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        response = request.render(
            'odoocms_admission_portal.account_registration', qcontext)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    def admission_signup(self, qcontext):
        if not qcontext.get('token'):
            # our custom function should not be called if user go for reset password. So, we have added this statement
            # """ Shared helper that creates a res.partner out of a token """
            values = {key: qcontext.get(key) for key in (
                'login', 'name', 'password', 'email', 'phone', )}
            if not values:
                raise UserError(_("The form was not properly filled in."))
            # get all user and check if the email already exist or not
            user = request.env["res.users"].sudo().search([])
            count = 0
            for rec in user:
                if (rec.login).upper() == (qcontext.get("login")).upper():
                    count += 1
            if values.get('password') != qcontext.get('confirm_password'):
                raise UserError(
                    _("Passwords do not match; please retype them."))
            if count > 0:
                raise UserError(
                    _("Another user is already registered with same ."))
            # elif request.env["res.users"].sudo().search([("email", "=", qcontext.get("email")), ("mobile", "=", qcontext.get("mobile"))]):
            #     raise UserError(
            #         _("Another user is already registered with same Email or Mobile."))
            self._signup_with_values(qcontext.get('token'), values)
            request.env.cr.commit()
        else:
            res = super(AuthSignupHome, self).admission_signup(qcontext)
            # default will be called if you do have token---> means come here by clicking on reset password

    @http.route('/web/login/admission/', type='http', csrf=False, auth="public", sitemap=False)
    def web_login_admission(self, redirect=None, **kw):
        main.ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return http.redirect_with_hash(redirect)

        if not request.uid:
            request.uid = odoo.SUPERUSER_ID

        values = request.params.copy()
        country_id = request.env['res.country'].sudo().search([])
        values.update({
            'country_id': country_id,
        })
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            try:
                uid = request.session.authenticate(
                    request.session.db, kw['login'], str(kw['password']).strip())
                request.params['login_success'] = True
                current_user = request.env['res.users'].search(
                    [('id', '=', uid)])

                student_application = request.env['odoocms.application'].sudo().search(
                    [('application_no', '=', current_user.login)])

                if student_application:
                    # raise UserError('Login Detail Send By Email')
                    # return http.local_redirect('/admission/student/dashboard')
                    return http.local_redirect('/admission/application/')
                return http.redirect_with_hash(self._login_redirect(uid, redirect=redirect))

            except odoo.exceptions.AccessDenied as e:
                career_id = request.env['odoocms.admission.register'].sudo().search(
                    [('state', '=', 'application')]).career_id
                country_id = request.env['res.country'].sudo().search([])
                values.update({
                    'country_id': country_id,
                    'career_id': career_id,
                    'company': request.env.company

                })

                request.uid = old_uid
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _(
                    'Only employee can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        # otherwise no real way to test debug mode in template as ?debug =>
        # values['debug'] = '' but that's also the fallback value when
        # missing variables in qweb
        if 'debug' in values:
            values['debug'] = True

        response = request.render(
            'odoocms_admission_portal.account_registration', values)
        response.headers['X-Frame-Options'] = 'DENY'

        # website web_login function
        if not redirect and request.params['login_success']:
            if request.env['res.users'].browse(request.uid).has_group('base.group_user'):
                redirect = b'/web?' + request.httprequest.query_string
            else:
                redirect = '/admission/application/'
            return http.redirect_with_hash(redirect)

        # auth_signup web_login function
        response.qcontext.update(self.get_auth_signup_config())
        if request.httprequest.method == 'GET' and request.session.uid and request.params.get('redirect'):
            # Redirect if already logged in and redirect param is present
            return http.redirect_with_hash(request.params.get('redirect'))

        return response
