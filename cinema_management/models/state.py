from odoo import fields, models, api

class State(models.Model):
    _inherit = 'state'

    def create(self, vals):
        res = super(State, self).create(vals)
        return res
