from odoo import api, fields, models



class ShipmentTypes(models.Model):
    _name = "shipment.types"
    _description = 'Shipment Information'
    _rec_name = "shipment_name"

    shipment_name=fields.Char(string="Name")

    #Create a Vehicles
class Vehicles(models.Model):
    _name = "transport.vehicle"
    _description = "Transport Vehicles"

    # Define a Many2one field to link to the fleet.vehicle model
    fleet_vehicle_id = fields.Many2one('fleet.vehicle', string="Fleet Vehicle")

    # Fetch fields from fleet.vehicle to display as related fields
    name = fields.Char(related="fleet_vehicle_id.name", string="Vehicle Name")
    license_plate = fields.Char(related="fleet_vehicle_id.license_plate", string="License Plate")
    driver_id = fields.Many2one(related="fleet_vehicle_id.driver_id", string="Driver")
    model_id = fields.Many2one(related="fleet_vehicle_id.model_id", string="Model")
    color = fields.Char(related="fleet_vehicle_id.color", string="Color")
    odometer = fields.Float(related="fleet_vehicle_id.odometer", string="Odometer")
    fuel_type = fields.Selection(related="fleet_vehicle_id.fuel_type", string="Fuel Type")
    seats = fields.Integer(related="fleet_vehicle_id.seats", string="Seats")


