from odoo import models, fields, api

class BookCategory(models.Model):
    _name = 'book.category'
    _description = 'my_library.library_book_category'

    name = fields.Char(string='Category')
    description = fields.Text(string='Description')

    book_ids = fields.Many2many(
        comodel_name = 'library.book',
        string = 'Books')
    total_books = fields.Integer(string='Total Book(s)', compute="_compute_total_book")

    @api.depends("book_ids")
    def _compute_total_book(self):
        for record in self:
            record.total_books = len(record.book_ids)
