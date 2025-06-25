from odoo import models, fields
                        #TransientModel is a temporary model Records created in a TransientModel automatically 
                        # get deleted after some time (usually after the session ends or a few hours).
                        # Perfect for wizards, pop-ups, or short tasks.
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ticket_price = fields.Float(string='Ticket price', config_parameter='cinema_management.ticket_price')
