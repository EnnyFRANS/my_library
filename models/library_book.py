from odoo import models, fields, api, _
from odoo.tools.sql import SQL
from odoo.exceptions import ValidationError, UserError

class LibraryBook(models.Model):
    _name = 'library.book'
    # order by this way doesn't work
    _order = "name DESC"
    _description = 'my_library.library_book'


    active = fields.Boolean(string='Active')
    name = fields.Char(string='Name')
    author = fields.Char(string='Author')
    publication_date = fields.Date(string='Publication Date')
    summary = fields.Char(string='Summary')
    pages = fields.Integer(string='Pages')
    isbn = fields.Char(string='ISBN')
    sequence = fields.Integer(default=10)
    state = fields.Selection(
        string = 'State',
        selection=[('available','Available'),('borrowed', 'Borrowed'),('lost', 'Lost')],
                              help="selection for book's state")

    cover = fields.Binary(string='Cover')
    price = fields.Float (string='Price')
    member_ids = fields.One2many(
        comodel_name ='library.member',
        inverse_name='book_id',
        string ="Interested Members")
    tag_ids = fields.Many2many(
        comodel_name = 'library.book.tag',
        string = 'tag')
    category_ids = fields.Many2many(
        comodel_name='book.category',
        string = 'Categories')
    quantity = fields.Integer(string='quantity')
    loan_ids = fields.One2many(
        comodel_name ='library.loan',
        inverse_name ='book_id',
        string = 'Loans'
    )
    age_limit = fields.Integer('Minimum age')


    _sql_constraints = [('book_name_uniq', "unique(name)", "Book name must be unique.")]

    def change_book_status(self):
        if self.quantity > 0:
            self.state="available"
        elif self.quantity == 0:
            self.state = "borrowed"
        else: self.state ="lost"

    @api.onchange("quantity")
    def _onchange_quantity(self):
        self.change_book_status()

    def action_add_book(self):
        self.quantity += 1
        self.change_book_status()

    @api.constrains('publication_date')
    def _check_publication_date(self):
        for book in self:
            if book.publication_date > fields.Date.today():
                raise ValidationError(_('invalid date'))


