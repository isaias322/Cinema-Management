# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MovieTheater(models.Model):
    _name = 'movie.theater'
    _description = 'Movie Theater'
    # for adding chatter
    _inherit = ['mail.thread', 'mail.activity.mixin']
                                     # change to be track in chatter
    name = fields.Char(string='Name', tracking=True)
    address = fields.Char(string='Address')
    is_vip = fields.Boolean(string='Is VIP', compute = '_compute_is_vip', store= True)
    customer_ids = fields.Many2many('res.partner', string='Customers', compute='_compute_customer_ids', store=True)
    available_movie_ids = fields.Many2many('cinema.movie', string='Available movies')
    theater_room_ids = fields.One2many('theater.room', 'movie_theater_id',string='Theater rooms', tracking=True)
    movie_showing_ids = fields.One2many('movie.showing', 'movie_theater_id', string='Movie showings')
    bestselling_movie_ids = fields.Many2many('cinema.movie', string='Popular Movies',
                                             compute='_compute_bestselling_movie_ids')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    total_sales = fields.Float(string='Total sales', compute= '_compute_total_sales')
    
    # for calculating the total sale from all theaters.
    
    def _compute_total_sales(self):#sudo() in Odoo is used to temporarily bypass security rules and access rights,
                                   # allowing you to perform actions as an administrator, it gives full access.
        movie_theater = self.env['movie.theater'].sudo().search([])
        for theater in self:
            theater.total_sales = sum(movie_theater.mapped('movie_showing_ids.line_ids.order_id.amount_total'))
    
    @api.depends('available_movie_ids', 'available_movie_ids.showing_ids')
    #compute means to calculate the result of.
    def _compute_bestselling_movie_ids(self):
        for theater in self:                                            # The sorted() function returns a sorted list of the specified iterable object.
            theater.bestselling_movie_ids = theater.available_movie_ids.sorted(lambda mov: sum(mov.mapped('showing_ids.total_attendees')), reverse=True)

    @api.depends("movie_showing_ids", "movie_showing_ids.line_ids")
    def _compute_customer_ids(self):
        for theater in self:       # Mapped function is used when u need to add 2 more relation
            theater.customer_ids = theater.mapped('movie_showing_ids.line_ids.customer_id')

    @api.depends("theater_room_ids", 'theater_room_ids.has_vip_seats')
    def _compute_is_vip(self):
        for theater in self:  #filter() is a built-in function used for filtering elements from an iterable (like a list, tuple, or set) based on a specified condition.
                              #lambda is a keyword used to create small, anonymous functions.  
            if theater.theater_room_ids.filtered(lambda room: room.has_vip_seats):    
                theater.is_vip = True
            else:
                theater.is_vip = False

