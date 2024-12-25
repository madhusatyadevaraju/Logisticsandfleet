
import requests
from odoo import api, fields, models
from odoo.exceptions import UserError


class TransportEntry(models.Model):
    _name = "transport.entry"
    _rec_name = "tracking_number"

    customer_name=fields.Many2one('res.partner',string="Customer Name")
    stock_picking_id = fields.Many2one('stock.picking', string="Delivery Order", required=True)
    transporter_id = fields.Many2one('transport.transporters', string="Transported By")

    state = fields.Selection([('start', 'Start'),
                              ('waiting', 'Waiting'), ('in-progress', 'In-Progress'), ('delivery', 'Delivery'),("cancel","Cancelled")],
                             string="State",default="start")

    vehicle_id = fields.Many2one('transport.vehicle', string="Vehicle")
    # driver_id = fields.Many2one('res.partner', string="Driver")  # Assuming driver is a partner
    #shipment_type = fields.Many2one('shipment.types', string="Shipment Type")
    pickup_date = fields.Datetime(string="Transport Date")
   # arrived_date = fields.Datetime(string="Arrived Date")
    tracking_number=fields.Char(string="Tracking Number")
    lr_number=fields.Char(string="LR NUmber")
    no_of_parcels = fields.Integer(string="No Of Parcels")
    shipment_route=fields.Many2one('transport.routes',string="Transport Route")

    location_details_ids=fields.One2many('transport.location.details','demo_id',string="Location Details",readonly=True)


    def action_start(self):
        self.state="in-progress"
        for location in self.location_details_ids:
            location.start_time = fields.Datetime.now()
        self._update_location_state('in-progress')
        self._populate_transport_location_details()

    def action_waiting(self):
        self.state="waiting"
        self._update_location_state('waiting')
        self._populate_transport_location_details()

    def action_delivery(self):
        self.state="delivery"
        for location in self.location_details_ids:
            location.end_time = fields.Datetime.now()
        self._update_location_state('delivery')
        self._populate_transport_location_details()

    def action_cancel(self):
        self.state="cancel"
        self._update_location_state('cancel')
        self._populate_transport_location_details()

    def _update_location_state(self,new_state):
        for rec in self.location_details_ids:
            rec.state=new_state


    #It Will use for the Every time one entry is there I setted a default state is start
    @api.model
    def create(self, vals):
        """ Override create method to set default state 'start' for location details """
        record = super(TransportEntry, self).create(vals)
        # Fetch the related location details from the selected route
        if record.shipment_route and record.shipment_route.location_ids:
            # Create independent copies of location details for this transport entry
            new_location_details = []
            for location in record.shipment_route.location_ids:
                new_location_details.append((0, 0, {
                    'source_location': location.source_location.id,
                    'destination_location': location.destination_location.id,
                    'distance': location.distance,
                    'transport_charges': location.transport_charges,
                    'time_hours': location.time_hours,
                    # 'start_time': location_detail.start_time,
                    # 'end_time': location_detail.end_time,
                    'tracking_number':location.tracking_number,
                    'state': "start",
                }))
            # Now, update the transport entry record with the new location details
            record.write({'location_details_ids': new_location_details})
        return record


    #The details from the transport entry ->transport.location.details populated into stock->transport.location.details
    def _populate_transport_location_details(self):
        """ Populate transport location details in stock picking """
        if self.stock_picking_id:
            picking = self.stock_picking_id
            # Clear existing location details in stock.picking
            picking.transport_routes_ids = [(5, 0, 0)]  # Clears all One2many records

            # Add location details from transport.entry to stock.picking
            for location_detail in self.location_details_ids:
                picking.transport_routes_ids = [(0, 0, {
                    'source_location': location_detail.source_location.id,
                    'destination_location': location_detail.destination_location.id,
                    'distance': location_detail.distance,
                    'transport_charges': location_detail.transport_charges,
                    'time_hours': location_detail.time_hours,
                    'start_time': location_detail.start_time,
                    'end_time': location_detail.end_time,
                    'tracking_number':location_detail.tracking_number,
                    'state': location_detail.state,

                })]





