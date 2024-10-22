from importlib.resources import _

from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"


    transporter_info=fields.Many2one('transport.transporters',string="Transporter Info")

    vehicle_id = fields.Many2one('transport.vehicle', string="Vehicle")
    shipment_type = fields.Many2one('shipment.types', string="Shipment Type")
    pickup_date = fields.Datetime(string="Pickup Date")
    # driver_id = fields.Many2one('res.partner', string="Driver")  # Assuming driver is a partner
    shipment_route = fields.Many2one('transport.routes',string="Shipment Route")
    arrived_date = fields.Datetime(string="Arrived Date")
    is_shipment_details_added = fields.Boolean(string="Shipment Details Added", default=False)

    shipment_count = fields.Integer(string="Shipment", default=0,readonly=True)

    #Based on the shipment_route the transporter id will be fetched
    @api.onchange('shipment_route')
    def _onchange_shipment_route(self):
        if self.shipment_route:
            # Automatically fetch and set transporter info based on the selected route
            self.transporter_info = self.shipment_route.transporter_id  # Assuming `transporter_id` field exists in `transport.routes`

    def action_view_shipments(self):
        print("Hello")
    #
    #     # Create a new transport entry with details from the sale order
    #     self.env['transport.entry'].create({
    #         'sale_order_id': self.id,
    #         'transporter_id': self.transporter_info.id,
    #         'vehicle_id': self.vehicle_id.id,
    #         'driver_id': self.driver_id.id,
    #         'shipment_type': self.shipment_type.id,
    #         'pickup_date': self.pickup_date,
    #         'arrived_date': self.arrived_date,
    #     })
    #     # Redirect to the `transport.entry` model to show related records
    #     return {
    #         'name': 'Transport Entries',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'transport.entry',
    #         'view_mode': 'tree,form',
    #         # 'domain': [('vehicle_id', '=' ,self.vehicle_id.id),],
    #          'domain': [('sale_order_id', '=', self.id)],  # Filter entries by the current sale order
    #         'context': dict(self.env.context, create=False),
    #     }



    # opens a form view for the shipment.details.wizard
    def action_view_shipment_details(self):
        self.is_shipment_details_added=True
        return {
            'name': 'Shipment Details',
            'type': 'ir.actions.act_window',
            'res_model': 'shipment.details.wizard',
            'view_mode': 'form',
            'target': 'new',  # Opens in a modal
            'context': {'default_order_id': self.id,
                        'default_shipment_count': self.shipment_count},  # You can pass default values if needed
        }


    def action_confirm(self):
        # Check if shipment details have been added
        if not self.is_shipment_details_added:
            raise UserError(_("Please add shipment details before confirming the order."))

        # Proceed with the regular confirm action
        result = super(SaleOrder, self).action_confirm()
        print(self.shipment_count)

        # Fetch details into stock.picking after confirming
        for picking in self.picking_ids:
            #self.picking_ids contains all the stock.picking records (deliveries) related to the sale order.
            picking.transporter_info = self.transporter_info
            picking.vehicle_id = self.vehicle_id
            picking.shipment_type = self.shipment_type
            picking.pickup_date = self.pickup_date
            # picking.driver_id = self.driver_id
            picking.shipment_route = self.shipment_route
            picking.arrived_date = self.arrived_date
            picking.shipment_count=self.shipment_count
        return result

