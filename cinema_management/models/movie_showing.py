# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MovieShowing(models.Model):
    _name = 'movie.showing'
    _description = 'Movie Showing'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    #for the default price to work in the setting.
    def _default_ticket_price(self):
        ticket_price = self.env['ir.config_parameter'].sudo().get_param('cinema_management.ticket_price')
        return round(float(ticket_price), 2)

    movie_id = fields.Many2one('cinema.movie', string='Movie')
    movie_theater_id = fields.Many2one('movie.theater', string='Movie theater')
    theater_room_id = fields.Many2one('theater.room', string='Theater room')
    seats_number = fields.Integer(related='theater_room_id.seats_number', store=True)
    line_ids = fields.One2many('movie.showing.line','showing_id',  string='Attendees')
    total_attendees = fields.Integer(string='Total audience', compute='_compute_total_attendees', store=True)
    date_start = fields.Datetime(string='Date start')
    date_end = fields.Datetime(string='Date end')# Use a dynamic default value by calling the _default_ticket_price 
                                                 #function when creating a new record.
    ticket_price = fields.Float(string='Ticket price', default=lambda self: self._default_ticket_price(), 
                                tracking=True)
    # compute: The field’s value is automatically calculated by Python code, instead of being entered by the user.
    is_past = fields.Boolean(string="Is past", compute='_compute_is_past')
    status = fields.Selection([('open', 'Open'), ('playing', 'Playing'), ('ended', 'Ended')], default='open')

    #when someone tries to update a record
    def write(self, vals):
        if vals and 'status' in vals:
            if self.env.user.has_group('cinema_management.cinema_manager_user_group'):
                raise ValidationError('Only managers can modify the showing status ')
        # If the user is allowed OR 'status' is not being changed, continue to update the record
        res = super(MovieShowing, self).write(vals)
        return res

    def _compute_is_past(self):
        for showing in self:
            if showing.date_start:  # ✅ Check if the date exists
                showing.is_past = showing.date_start < fields.Datetime.now().replace(hour=0, minute=0, second=0)
            else:
                showing.is_past = False  # If date is empty, consider it as not past


    # Chained Domain: The options available in one field depend on what you select in another field.
    def _update_showing_price(self):
        sci_showings = self.env['movie.showing'].search([('movie_id.category', '=', 'sci_fi')])
        sci_showings.write({'ticket_price': 12})
        action_showings = self.env['movie.showing'].search([('movie_id.category', '=', 'action')])
        action_showings.write({'ticket_price': 15})
        comedy_showings = self.env['movie.showing'].search([('movie_id.category', '=', 'comedy')])
        comedy_showings.write({'ticket_price': 8})
        thriller_showings = self.env['movie.showing'].search([('movie_id.category', '=', 'thriller')])
        thriller_showings.write({'ticket_price': 9})
        other_showings = self.env['movie.showing'].search([('movie_id.category', 'not in', ['sci_fi', 'action', 'comedy', 'thriller'])])
        other_showings.write({'ticket_price': 10})
                  # for adding a record to a record set we use |
        showings = sci_showings | action_showings | comedy_showings | thriller_showings | other_showings
        # for logging custom messages
        for showing in showings:
            showing.message_post(body='The scheduled action was executed')

    @api.depends('line_ids')
    def _compute_total_attendees(self):
        for showing in self:
            showing.total_attendees = len(showing.line_ids)


class MovieShowingLines(models.Model):
    _name = 'movie.showing.line'
    _description = 'Movie Showing Line'

    showing_id = fields.Many2one('movie.showing', string='Movie Showing')
    customer_id = fields.Many2one('res.partner', string='Customer')
    order_id = fields.Many2one('sale.order', string='Sale order')
    state = fields.Selection([('attended', 'Attended'), ('canceled', 'Canceled')], string='State', default='attended')

    # This method runs when a new Movie Showing Line is created.
    # It also automatically creates a new Sale Order for the selected customer.
    # For the ticket price to show in sales moduel
    def create(self, vals):
        res = super(MovieShowingLines, self).create(vals) # Create the Movie Showing Line record.
        for line in res:
            order = self.env['sale.order'].with_context(ticket_price=res.showing_id.ticket_price).create(
                {'partner_id': line.customer_id.id}) #with_context is used to pass extra information
        line.order_id = order
        return res       #(called context) when performing an action, without changing the main logic of the method.