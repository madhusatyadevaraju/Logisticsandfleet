from email.policy import default

from odoo import api, fields, models


class TransportLocation(models.Model):
    _name = "transport.location"
    _rec_name = "location"


    location=fields.Char(string="Locations")

class TransportLocationDetails(models.Model):
    _name = "transport.location.details"

    #Location Details
    route_id=fields.Many2one('transport.routes' ,string="Routes")
    source_location=fields.Many2one('transport.location',string="Source Location")
    destination_location = fields.Many2one('transport.location', string="Destination Location")
    distance=fields.Float(string="Distance(KM)")
    transport_charges=fields.Float(string="Transport Charges")
    time_hours=fields.Float(string="Time Taken")
    picking_id = fields.Many2one('stock.picking', string="Picking Reference")
    transport_id=fields.Many2one('transport.entry',string="Transport Entry")
    demo_id=fields.Many2one('transport.entry')

    # Add fields some fields
    start_time=fields.Datetime(string="Start Time",default=False)
    end_time=fields.Datetime(string="End Time" , default=False)
    tracking_number=fields.Char(string="Tracking Number")
    state = fields.Selection([('start', 'Start'),
                              ('waiting', 'Waiting'), ('in-progress', 'In-Progress'), ('delivery', 'Delivery'),
                              ("cancel", "Cancelled")],
                             string="State", default="start")
    _sql_constraints = [
        ('unique_route_per_transporter', 'unique(source_location, destination_location, route_id)',
         'Location details for the same source and destination already exist for this route!')
    ]


    # @api.model
    # def create(self, vals):
    #     # Ensure the state defaults to 'start' for each new entry
    #     vals.setdefault('state', 'start')
    #     return super(TransportLocationDetails, self).create(vals)

