import logging
from base64 import b64decode
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
    _description = "Importador Xml Flamero"

    data_file_partner = fields.Binary(
        string="File to Import",
        required=False,
        help="Get you data from xml file.",
    )
    filename = fields.Char()

    def _import_partner(self, data_file_partner):
        print("PARO A IMPORTAR UN partner")
