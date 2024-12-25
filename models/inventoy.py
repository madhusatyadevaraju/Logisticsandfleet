from email.policy import default

from odoo import api, fields, models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    transporter_info = fields.Many2one('transport.transporters', string="Transporter Info")
    shipment_type = fields.Many2one('shipment.types', string="Shipment Type")
    vehicle_id = fields.Many2one('transport.vehicle', string="Vehicle")
    # driver_id = fields.Many2one('res.partner', string="Driver")  # Assuming driver is a partner
    shipment_route = fields.Many2one('transport.routes', string="Shipment Route")
    pickup_date = fields.Datetime(string="Pickup Date")
    arrived_date = fields.Datetime(string="Arrived Date")

    lr_number=fields.Char(string="LR Number")
    no_of_parcels=fields.Integer(string="No Of Parcels")

    shipment_count = fields.Integer(string="Shipment",default=0,readonly=True)
    tracking_number=fields.Char(string="Tracking Number")
    transport_routes_ids = fields.One2many(
        'transport.location.details', 'picking_id', string="Transport Routes"
    )
    # routes_ids=fields.Many2one('transport.routes',string="Transport Routes")

    #This action button is used to to populate the details from stock to tranport entry
    def action_view_shipments(self):
        print("hello")
        # Create a new transport entry with details from the sale order
        transport_entry=self.env['transport.entry'].create({
            'stock_picking_id': self.id,
            'transporter_id': self.transporter_info.id,
            'vehicle_id': self.vehicle_id.id,
            # 'driver_id': self.driver_id.id,
            # 'shipment_type': self.shipment_type.id,
            'pickup_date': self.pickup_date,
            # 'arrived_date': self.arrived_date,
            'tracking_number':self.tracking_number,
            'customer_name':self.partner_id.id,
            'lr_number':self.lr_number,
            'no_of_parcels':self.no_of_parcels,
            'shipment_route':self.shipment_route.id,

        })
        # Fetch transport location details based on the new transport entry and populate tracking number
        if transport_entry:
            # Update the transport location details with the tracking number
            for location in transport_entry.location_details_ids:
                location.tracking_number = self.tracking_number
        # Redirect to the `transport.entry` model to show related records
        return {
            'name': 'Transport Entries',
            'type': 'ir.actions.act_window',
            'res_model': 'transport.entry',
            'view_mode': 'tree,form',
            'domain': [('stock_picking_id', '=', self.id)],  # Filter entries by the sale order
            'context': dict(self.env.context, create=False),
        }

    # @api.onchange('routes_ids')
    # def _onchange_transport_routes(self):
    #     if self.routes_ids:
    #         # Fetch related transport location details for the selected route
    #         related_details = self.env['transport.location.details'].search([
    #             ('route_id', '=', self.routes_ids.id)
    #         ])
    #
    #         # Assign the fetched details to transport_route_ids
    #         for rec in related_details:
    #             self.transport_routes_ids = [(5, 0, 0)]  # Clear existing records
    #             self.transport_routes_ids = [(0, 0, {
    #             'source_location': rec.source_location.id,
    #             'destination_location': rec.destination_location.id,
    #             'distance': rec.distance,
    #             'transport_charges': rec.transport_charges,
    #             'time_hours': rec.time_hours,
    #         })]
    #     else:
    #         # Clear transport_route_ids if no transport route is selected
    #         self.transport_route_ids = [(5, 0, 0)]
     #Tracking NUmber
    @api.model
    def create(self, vals):
        # Set the tracking number using the sequence if not already set
        if not vals.get('tracking_number'):
            vals['tracking_number'] = self.env['ir.sequence'].next_by_code('stock.picking.tracking') or 'New'
        return super(StockPicking, self).create(vals)

    def button_validate(self):
        # Check if the tracking number is already set
        if not self.tracking_number:
            # Assign the tracking number using the sequence
            self.tracking_number = self.env['ir.sequence'].next_by_code('stock.picking.tracking') or 'New'


        # Call the original button_validate method
        return super(StockPicking, self).button_validate()



    # Define the sequence for tracking numbers
    class IrSequence(models.Model):
        _inherit = 'ir.sequence'

        @api.model
        def _get_default_stock_picking_tracking(self):
            return {
                'name': 'Stock Picking Tracking Sequence',
                'code': 'stock.picking.tracking',
                'padding': 4,
                'prefix': 'TRA/',
            }
