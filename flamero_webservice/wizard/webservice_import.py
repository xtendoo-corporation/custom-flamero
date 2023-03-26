import logging
from base64 import b64decode
from io import StringIO

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

    def web_service_get(self):
        result = self.webservice_backend_id.call("get")

        for row in result:
            print("-------------------------------------------")
            print("row:", row)
            print("-------------------------------------------")

            email = row[6]

            if email is not None:
                mail_contact = self.env["mailing.contact"].search([("email", "=", email), ])

                if not mail_contact:
                    nombre = row[0]
                    apellido_1 = row[1]
                    apellido_2 = row[2]
                    nombre_completo = nombre

                    if apellido_1 is not None:
                        nombre_completo = nombre_completo + " " + apellido_1

                    if apellido_2 is not None:
                        nombre_completo = nombre_completo + " " + apellido_2

                    self.env["mailing.contact"].sudo().create({
                        'email': email,
                        'name': nombre_completo,
                        'company_name': nombre_completo,
                    })
                else:
                    print("*" * 80)
                    print("Email " + email + " ya pertenece a la base de datos.")
                    print("*" * 80)
        return

        # with self.assertRaises(exceptions.ConnectionError):
        #     self.webservice_backend_id.call("get")

