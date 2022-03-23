import base64
import logging
import re
import xml.dom.minidom
from lxml import etree
from io import StringIO

from odoo import _, api, fields, models
from requests import auth, exceptions


_logger = logging.getLogger(__name__)

class XmlFlameroImport(models.TransientModel):
    _name = "xml.flamero.import"
    _description = "Importador Xml Flamero"

    data_file_xml = fields.Binary(
        string="File to Import",
        required=False,
        help="Get you data from xml file.",
    )
    filename = fields.Char()

    def import_file(self):
        """ Process the file chosen in the wizard, create bank statement(s) and go to reconciliation. """
        self.ensure_one()

        print("paso a importar el fichero")

        # datasource = open(self.filename)
        # datasource = b64decode(self.filename)
        # if data_file_agentes:
        #     # self._import_agentes(data_file_agentes)
        #     print(datasource)
        #     content = xml.dom.minidom.parseString(datasource)
        #     print(content)

        print(self.filename)
        generated_facturae = etree.fromstring(base64.urlsafe_b64decode(self.filename))
        print(generated_facturae)

        # self.assertEqual(
        #     generated_facturae.xpath(
        #         "/fe:Facturae/Parties/SellerParty/TaxIdentification/"
        #         "TaxIdentificationNumber",
        #         namespaces={"fe": self.fe},
        #     )[0].text,
        #     self.env.ref("base.main_company").vat,
        # )

        # for val in ["w:p", "w:h", "text:list"]:
        #     for element in content.getElementsByTagName(val):
        #         buf += textToString(element) + "\n"

    def decode_base64(data, altchars=b'+/'):
        """Decode base64, padding being optional.

        :param data: Base64 data as an ASCII byte string
        :returns: The decoded byte string.

        """
        data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
        missing_padding = len(data) % 4
        if missing_padding:
            data += b'='* (4 - missing_padding)
        return b64decode(data, altchars)
