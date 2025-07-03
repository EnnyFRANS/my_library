# -*- coding: utf-8 -*-

from . import controllers
from . import models
from . import wizard

def hook_duration_post_init(env):
    env['ir.config_parameter'].set_param('library_loan.duration','90')
