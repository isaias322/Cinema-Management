# -*- coding: utf-8 -*-
{
    'name': "Cinema Management",
    'summary': "Manages the logistic and sales of a multiple movie theaters with odoo",
    'author': "Isaias Younison",
    'version': '18.0.0.1',
    "category": "Movies",
    "price": 100,
    "currency": "USD",
    "license": "AGPL-3", #To include a module in your module
    'depends': ['base', 'sale'],
    "application": True,
    'data': [
        'security/ir.model.access.csv',
        'security/cinema_management_security.xml',
        'views/movie_theater_views.xml',
        'views/theater_room_views.xml',
        'views/movie_showing_views.xml',
        'views/cinema_movie_views.xml',
        'views/customer_views.xml',
        'views/res_config_settings_views.xml',
        'views/movie_review_views.xml',
        'data/ir_actions.xml',
    ],
    "images": ['picture/image.png'],
    "installable": True,
    "auto_install": False,
}