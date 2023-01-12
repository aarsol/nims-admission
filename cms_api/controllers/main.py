
from odoo.addons.base_rest.controllers import main

class BaseRestHUApiController(main.RestController):
    _root_path = "/nutech/"
    _collection_name = "nutech.services"
    _default_auth = 'api_key'  #"public"


class BaseRestPrivateApiController(main.RestController):
    _root_path = "/rest/private/"
    _collection_name = "base.rest.private.services"
    _default_auth = 'api_key'   #"user"

