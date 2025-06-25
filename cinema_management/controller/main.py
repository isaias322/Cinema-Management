from odoo.http import Controller, request, route
import json

class CinemaManagerController(Controller):

    @route(['/cinema/showings/',
            '/cinema/showings/<string:category>'], type='http', auth='public', methods=['GET'], csrf=False)
    def fetch_movie_showings(self, category=False, **kwargs):
        showings = request.env['movie.showing'].sudo().search([])
        if category:
            showings= showings.filtered(lambda showing: showing.movie_id.category == category)
        showings = [{'movie': showing.movie_id.name} for showing in showings]
        return request.make_response(json.dumps(showings))
    

    @route('/cinema/movie_theaters', type='json', auth='public', csrf=False)
    def fetch_movie_theaters(self, **kwargs):
        domain = []
        if kwargs.get('is_vip'):
            domain += [('is_vip', '=', True)]
        movie_theaters = request.env['movie_theater'].sudo().search(domain)
        movie_theaters = [{'name': theater.name}for theater in movie_theaters]
        return movie_theaters

