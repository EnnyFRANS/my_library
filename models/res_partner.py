from email.policy import default

from odoo import models, fields, api

class Partner(models.Model):
    _inherit = ['res.partner']

    is_member = fields.Boolean("Is member", default=True)