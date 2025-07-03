from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    loan_limit_days = fields.Integer(string="Total return days",
                                     config_parameter='library_loan.duration') #library.duration --> 'library_loan' can be named as key word in the field