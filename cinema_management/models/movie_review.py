from odoo import models, fields, api
from odoo.exceptions import UserError


class MovieReview(models.Model):
    _name = 'movie.review'
    _description = 'Movie Review'

    customer_id = fields.Many2many ('res.partner', string='Customer')
    movie_id = fields.Many2one('cinema.movie', string='Movie')
    rating = fields.Integer(string='Rating')
    customer_reviews = fields.Text(string='Review')
    staff_response = fields.Text(string='Response')

    #Constrain is a rule that restricts the allowed values of fields to ensure the data is correct and valid.
    # It is used to prevent incorrect data from being saved.
    @api.constrains('rating')
    def check_rating(self):
        for movie in self:
            if movie.rating < 1 or movie.rating > 10:
                raise UserError('Please enter a rating from 1 to 10')