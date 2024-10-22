from importlib.resources import _

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TransportRoutes(models.Model):
    _name = "transport.routes"
    _rec_name = "name"


    name = fields.Char(string="Name",compute="_compute_name",store=True)
    transporter_id= fields.Many2one('transport.transporters', string="Transporter")
    location_ids=fields.One2many('transport.location.details','route_id')

    #Based ON the Destination and Source Location The name field wil Be fetched
    @api.depends('location_ids.source_location', 'location_ids.destination_location')
    def _compute_name(self):
        for record in self:
            # Check if there are any locations
            if record.location_ids:
                # Fetch the first location to compute the name
                first_location = record.location_ids[0]
                if first_location.source_location and first_location.destination_location:
                    record.name = f"{first_location.source_location.location}-{first_location.destination_location.location}"
                else:
                    record.name = 'Specify Route Location'
            else:
                record.name = 'No Locations Defined'

    @api.constrains('location_ids')
    def _check_single_route_per_transporter(self):
        for record in self:
            if len(record.location_ids) > 1:
                raise ValidationError(
                    _("Only one route can be added for the transporter '%s'.") % record.transporter_id.name)
