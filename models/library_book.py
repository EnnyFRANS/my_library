from odoo import models, fields, api

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


