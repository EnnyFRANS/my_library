from odoo import api, fields, models, _

class ShowMemberInLoan(models.TransientModel):
    _name = 'show.member.in.loan'
    _description = 'Show member IDs with a button from loan page'

    member_id = fields.Many2one('library.member')
    return_date_due = fields.Date('Return date due')
    book_ids = fields.Many2many('library.book',
                              domain="[('state','=', 'available')]"
                              )
    creation_stage = fields.Selection(
        string='stages',
        selection=[('member', 'Member'),
                   ('selected_books', 'Selected_books'),
                   ('summary', 'Summary')])
    '''when pass an info to record, have to always  pass the id, example below: 
     book.id and member_id.id'''
    def action_create_loan(self):
        for book in self.book_ids:
            self.env['library.loan'].create({
                'book_id': book.id,
                'member_id': self.member_id.id
            })

    # see the example for default value : def _get_default_departure_date(self):
