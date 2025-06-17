from random import randint
from odoo import models, fields, api

class LibraryBookTag(models.Model):
    _name = 'library.book.tag'
    #_order = 'sequence,id'
    _description = 'my_library.library_book_tag'

    def _get_default_color(self):
        return randint(1, 11)

    active = fields.Boolean(string='Active')
    name = fields.Char(string='Name')
    color = fields.Integer(string='Color', default=_get_default_color, help="Transparent tags are not visible in the kanban view of your projects and tasks.")
