from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        if self._context.get('ticket_price'):
            self.env['sale.order.line'].create({'price_unit':self._context.get('ticket_price'),
                                                'name':res.name,
                                                'order_id':res.id})
        return res