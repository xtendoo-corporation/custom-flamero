import logging
from base64 import b64decode
from io import StringIO

import responses

from odoo import _, api, fields, models
from requests import auth, exceptions


_logger = logging.getLogger(__name__)

try:
    from csv import reader
except (ImportError, IOError) as err:
    _logger.error(err)


class FlameroWebserviceImport(models.TransientModel):
    _name = "flamero.webservice.import"
    _description = "Flamero Webservice Import"

    webservice_backend_id = fields.Many2one("webservice.backend")

    def import_file(self):
        """ Process the file chosen in the wizard, create bank statement(s) and go to reconciliation. """
        self.ensure_one()
        print("*"*80)
        print("Run Webservice:", self.webservice_backend_id.name )
        print("*"*80)
        self.web_service_get()

    @responses.activate
    def web_service_get(self):
        responses.add(responses.GET, self.webservice_backend_id.url, body="{}")
        self.webservice_backend_id.call("get")

        print("*"*80)
        print("Responses.calls:", len(responses.calls))
        print("Headers:", responses.calls[0].request.headers)
        data = auth._basic_auth_str(self.webservice_backend_id.username, self.webservice_backend_id.password)
        print("Data:", data)
        print("*"*80)



        # with self.assertRaises(exceptions.ConnectionError):
        #     self.webservice_backend_id.call("get")

