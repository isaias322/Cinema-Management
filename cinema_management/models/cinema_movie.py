# -*- coding: utf-8 -*-

from odoo import models, fields


class CinemaMovie(models.Model):
    _name = 'cinema.movie'
    _description = 'Movie'

    name = fields.Char(string='Name')
    category = fields.Selection([('sci_fi', 'Sci-fi'), ('thriller', 'thriller'),
                                 ('action', 'Action'), ('comedy', 'Comedy'),
                                 ('horror', 'Horror'), ('fantasy', 'Fantasy')], string='Category')
    rating = fields.Selection([('g_rating', 'G'), ('pg_rating', 'PG'), ('pg12_rating', 'PG-13'),
                               ('r_rating', 'R'), ('nc17_rating', 'NC-17')], string='Rating')
    showing_ids = fields.One2many('movie.showing', 'movie_id', string='Showings')
    review_ids = fields.One2many('movie.review', 'movie_id', string='Reviews')

    def action_update_response(self):
    # Loop through each movie record in the current model
        for movie in self:
            self._cr.execute("SELECT r.id, m.name, r.rating FROM movie_review r JOIN cinema_movie m " \
                             "ON r.movie_id = m.id WHERE r.movie_id = %s" % movie.id)
            # helps to make it faster and not slowing down the system
            reviews = self._cr.fetchall()
        # Loop through each review related to this movie
            for review in reviews: 
            # Check if the review rating is 6 or higher
                if review[2] >= 6:
                # Run a direct SQL query to update the staff_response for good reviews
                # %s is a placeholder that will be replaced by the review ID
                    self._cr.execute(
                    "UPDATE movie_review SET staff_response = 'Thank you for the review' "
                    "WHERE id = %s" % review[0]
                    )
                else:
                # Run a direct SQL query to update the staff_response for bad reviews
                # The message will include the movie name and the review ID
                    self._cr.execute(
                    "UPDATE movie_review SET staff_response = 'Sorry for your experience with the movie %s, "
                    "we hope you would have better experience in our theater with other movie' WHERE id = %s" % (review[1], review[0]))
            # Save the changes to the database after each update
                self._cr.commit()
