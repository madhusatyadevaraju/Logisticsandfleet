from importlib.resources import _

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TransportTransporters(models.Model):
    _name = "transport.transporters"
    _description = 'Transporter Information'

    name = fields.Char(string="Transport Name", required=True)
    contact_person = fields.Char(string="Contact Person", required=True)
    mobile = fields.Char(string="Mobile")
    email=fields.Char(string="Email")
    logo = fields.Binary(string="Company Logo")

    # Address fields
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street 2")
    city = fields.Char(string="City")
    state_id = fields.Many2one('res.country.state', string="State")
    zip = fields.Char(string="Zip")
    country_id = fields.Many2one('res.country', string="Country")

    #Transporter Details
    transporter=fields.Boolean(string="Transporter")
    # shipment_form=fields.Selection([("sale", "Sale"), ("picking", "Picking")], string="Shipment Form")
    driver=fields.Char(string="Driver")
    vehicle_id=fields.Many2one( 'transport.vehicle',string="Vehicle")
    routes=fields.Many2one('transport.routes',string="Routes")
    delivery_count = fields.Integer(compute='_compute_delivery_count', string="Delivery Count")

    @api.constrains('routes')
    def _check_route_transporter_match(self):
        for record in self:
            if record.routes:
                # Check if the transporter of the selected route matches the current transporter's name
                if record.routes.transporter_id and record.routes.transporter_id.name != record.name:
                    raise ValidationError(
                        _("This route is not matched to this transporter: %s") % record.routes.transporter_id.name)

    @api.onchange('vehicle_id')
    def _onchange_vehicle_id(self):
        if self.vehicle_id:
            self.driver = self.vehicle_id.driver_id.name  # Assuming driver_id is a Many2one field to a res.partner or driver model
        else:
            self.driver = False  # Clears the driver field if no vehicle is selected

    def _compute_delivery_count(self):
        for transporter in self:
            # Assuming stock.picking has a field 'transporter_id' that links it to transport.transporters
            transporter.delivery_count = self.env['stock.picking'].search_count(
                [('transporter_info', '=', transporter.id)])

    def action_view_stock_deliveries(self):
        """ Action to view stock deliveries related to this transporter """
        # Assuming stock.picking has a field 'transporter_id' to relate to this model
        print("Working")
        return {
            'name': 'Stock Deliveries',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'domain': [('transporter_info', '=', self.id)],  # Filter stock.picking by transporter
            'context': dict(self.env.context),
        }


