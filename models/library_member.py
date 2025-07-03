from reportlab.graphics.transform import inverse

from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.member'
    _description = 'my_library.library_member'

    @api.model
    def give_default_member_number(self):
        last_member = self.search([], order="member_number desc", limit=1)
        return last_member

    active = fields.Boolean(string='Active')
    name = fields.Char(string='Name')
    mail = fields.Char(string='E-mail')
    summary = fields.Char(string='Summary')
    phone = fields.Integer(string='Phone')
    member_number = fields.Integer(string='Member Number', default= give_default_member_number)
    member_age = fields.Integer('Age', default=0)

    subscription_date = fields.Date(string='Subscription date')
    book_id = fields.Many2one(
        comodel_name='library.book',
        string='favorite books')
    loan_ids = fields.One2many(
        comodel_name ='library.loan',
        inverse_name='member_id',
        string ="Loans",
        domain = ['|', ('state', '=', 'ongoing'), ('state', '=', 'late')],
    )
    loan_count = fields.Integer('Loan Count', compute='_compute_total_loan')

    @api.depends("loan_ids")
    def _compute_total_loan(self):
        for record in self:
            record.loan_count = len(record.loan_ids)

    def action_get_loans(self):
        return {
            'name':'Members Loans',
            'view_mode': 'list,form',
            'domain': [('state', '=', 'ongoing')],
            'res_model':'library.loan',
            'type': 'ir.actions.act_window',
        }






