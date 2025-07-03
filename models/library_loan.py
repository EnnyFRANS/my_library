from email.policy import default

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class LibraryLoan(models.Model):
    _name = 'library.loan'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']
    _description = 'my_library.library_loan'

    '''This is an example where we can put a default that create automatically the name by calling the library loan'''
    # name = fields.Char(string='Name', readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('my.library.loan'))
    # name = fields.Char(string='Name', readonly=True, default=lambda self: _('New'),)

    name = fields.Char('Name', readonly=True)

    active = fields.Boolean(string='Active', default=True)
    check_out_date = fields.Date(string='Check out date')
    subscription_date = fields.Date(string='Subscription date')
    return_date_due = fields.Date(string='return date due')
    return_date_effective = fields.Date(string='return date effective')
    state = fields.Selection(
        string='State',
        selection=[('ongoing', 'Ongoing'), ('returned', 'Returned'), ('late', 'Late')],
        help="selection for loan's state")
    member_id = fields.Many2one(
        comodel_name='library.member',
        string='Member')
    book_id = fields.Many2one(
        string='book',
        comodel_name='library.book')

    #Example
    @api.model_create_multi  # ----> a decorator obligation
    def create(self, vals_list):  #---self = the instance of the current class, vals_list=the list of dictionaries
        for vals in vals_list:    #---so here, vals is a single dictionary
            if not vals.get('book_id'):
                raise ValidationError("No book !")
        result = super().create(vals_list)   # this is when the database is affected (addition of new instance)
        for record in result:  # We do this after the creation to avoid doing the search in recorded data in library_book table
            record.book_id.quantity -= 1
            seq_number = self.env['ir.sequence'].next_by_code('my.library.loan')
            record.name = seq_number+record.book_id.name
        return result

    def write(self, vals):
        if vals.get('state') == 'returned':
            for record in self:
                record.active = False
                record.book_id.quantity += 1
        return super().write(vals)

    @api.model
    def cron_late_show_message_chatter(self):
        for record in self.search([]):
            if record.state=='late':
                record.message_post(body="This is the print with condition 'state=late'")

    #This is worked also
    # @api.model
    # def cron_late_show_message_chatter(self):
    #     for record in self.search([]):
    #         record.message_post(body="This is the print before condition 'state = late'")


    #Todo: to be continued
    # def action_send_message_details(self):
    #     for record in self.search([]):
    #         record.message_post(body="book")


    # @api.model
    # def default_get(self, fields):
    #     super

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'check_out_date' in fields_list:
            res['check_out_date'] = fields.Date.today()
        days_to_return = self.env['ir.config_parameter'].get_param('library_loan.duration')
        if 'return_date_due' in fields_list:
            res['return_date_due'] = fields.Date.add(fields.Date.today(), days=int(days_to_return))
        return res

    def action_open_wizard_see_member(self):
        return {
            'res_model':'show.member.in.loan',
            'view_mode' : 'form',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_member_id': self.member_id.id,
                        'default_return_date_due':self.return_date_due,
                        },
        }


    # see the example for default value : def _get_default_departure_date(self):

    # def set_loan_name(self):
    #     self.name = self.env['ir.sequence'].next_by_code('my.library.loan')
    #     return self.name
    book_ids_domain = fields.Many2many(comodel_name='library.book' ,compute='_compute_books_domain')

    @api.depends("member_id")
    def _compute_books_domain(self):
        for record in self:
            if record.member_id:
                age = record.member_id.member_age
                record.book_ids_domain = self.env['library.book'].search([('age_limit', '<=', age)])
            else:
                record.book_ids_domain = []











