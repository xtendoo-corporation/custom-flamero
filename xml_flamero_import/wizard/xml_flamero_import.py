import base64
import logging
from lxml import etree
from io import StringIO

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    from csv import reader
except (ImportError, IOError) as err:
    _logger.error(err)

class XmlFlameroImport(models.TransientModel):
    _name = "xml.flamero.import"
    _description = "Importador Flamero"

    data_file_xml = fields.Binary(
        string="File to Import",
        required=False,
        help="Get you data from xml file.",
    )
    invoice_file = fields.Binary(
        string="PDF or XML Invoice"
    )
    invoice_filename = fields.Char(
        string="Filename"
    )

    @api.model
    def get_parsed_invoice(self, invoice_file_b64):
        assert invoice_file_b64, "No invoice file"
        assert isinstance(invoice_file_b64, bytes)
        file_data = base64.b64decode(invoice_file_b64)
        decode = file_data.decode("utf-8")
        inicio = decode.find("Fichero") + 9
        fin = decode.find("ETag") - 3
        cadena_resultado = decode[inicio:fin]
        file_data = base64.b64decode(cadena_resultado)
        try:
            csv_data = reader(StringIO(file_data.decode("utf-8")))
        except Exception:
            raise UserError(_("Can not read the file"))

        for row in csv_data:

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

        # for entry in xml_root.xpath('ns:entry', namespaces={"ns": "http://www.w3.org/2005/Atom"}):
        #     content = entry.find('{http://www.w3.org/2005/Atom}content')
        #     properties = content.xpath("m:properties", namespaces={
        #         "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata"})
        #     email = properties[0].xpath("d:E_mail", namespaces={
        #         "d": "http://schemas.microsoft.com/ado/2007/08/dataservices"})
        #     if email is not None:
        #         mail_contact = self.env["mailing.contact"].search([("email", "=", email[0].text), ])
        #
        #         if not mail_contact:
        #             nombre = properties[0].xpath("d:Nombre",
        #                                     namespaces={"d": "http://schemas.microsoft.com/ado/2007/08/dataservices"})
        #             apellido_1 = properties[0].xpath("d:Apellido_1",
        #                                     namespaces={"d": "http://schemas.microsoft.com/ado/2007/08/dataservices"})
        #             apellido_2 = properties[0].xpath("d:Apellido_2",
        #                                     namespaces={"d": "http://schemas.microsoft.com/ado/2007/08/dataservices"})
        #             nombre_completo = nombre[0].text
        #
        #             if apellido_1[0].text is not None:
        #                 nombre_completo = nombre_completo + " " + apellido_1[0].text
        #
        #             if apellido_2[0].text is not None:
        #                 nombre_completo = nombre_completo + " " + apellido_2[0].text
        #
        #             self.env["mailing.contact"].sudo().create({
        #                 'email': email[0].text,
        #                 'name': nombre_completo,
        #                 'company_name': nombre_completo,
        #             })
        #         else:
        #             print("*" * 80)
        #             print("Email " + email[0].text + " ya pertenece a la base de datos.")
        #             print("*" * 80)

    def import_file(self):
        self.ensure_one()
        self.get_parsed_invoice(self.invoice_file)
