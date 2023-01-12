
import logging
import pdb

from odoo.http import request
from odoo import models
from werkzeug.exceptions import BadRequest
from odoo.exceptions import AccessDenied

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _auth_method_api_key(cls):
        user_key = request.httprequest.headers.get("username")
        if not user_key:
            raise BadRequest("Authorization header with username key missing")
        pass_key = request.httprequest.headers.get("password")
        if not pass_key:
            raise BadRequest("Authorization header with password key missing")

        # request.uid = 1
        # uid = request.env["auth.api.key"]._retrieve_uid_from_api_key(api_key)
        user_id = request.env['res.users'].sudo().search([('login', '=', user_key), ('secret', '=', pass_key)])
        if not user_id:
            raise BadRequest("API key invalid")

        request.uid = user_id.id
        return True

        # headers = request.httprequest.environ
        # api_key = request.httprequest.headers.get("Authorization")
        # if not api_key:
        #     raise BadRequest("Authorization header with API key missing")
        #
        # user_id = request.env["res.users.apikeys"]._check_credentials(
        #     scope="rpc", key=api_key
        # )
        # if not user_id:
        #     raise BadRequest("API key invalid")
        #
        # request.uid = user_id
        
        
        
        
        
        
        # api_key = headers.get("HTTP_API_KEY")
        # if api_key:
        #     request.uid = 1
        #     uid = request.env["auth.api.key"]._retrieve_uid_from_api_key(api_key)
        #     if uid:
        #         # reset _env on the request since we change the uid...
        #         # the next call to env will instantiate an new
        #         # odoo.api.Environment with the user defined on the
        #         # auth.api_key
        #         request._env = None
        #         request.uid = uid
        #         request.auth_api_key = api_key
        #         return True
        # _logger.error("Wrong HTTP_API_KEY, access denied")
        # raise AccessDenied()
