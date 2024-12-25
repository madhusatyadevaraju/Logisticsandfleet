from odoo import models, fields, api

class ShipmentDetailsWizard(models.TransientModel):
    _name = 'shipment.details.wizard'
    _description = 'Shipment Details Wizard'

    vehicle_id = fields.Many2one('transport.vehicle', string="Vehicle", required=True)
    shipment_type = fields.Many2one('shipment.types',string="Shipment Type")
    pickup_date = fields.Datetime(string="Pickup Date", required=True)
    # driver_id = fields.Many2one('res.partner', string="Driver", required=True)  # Assuming driver is a partner
    # shipment_route = fields.Many2one('transport.routes',string="Shipment Route", required=True)
    arrived_date = fields.Datetime(string="Arrived Date")


    def action_confirm(self):

        # Get the active sale order
        sale_order = self.env['sale.order'].browse(self._context.get('active_id'))
        shipment_count=self._context.get('default_shipment_count')
        shipment_count=shipment_count+1
        # Assign the wizard data to the sale order
        sale_order.write({
            'vehicle_id': self.vehicle_id.id,
            'shipment_type': self.shipment_type.id,
            'pickup_date': self.pickup_date,
            # 'driver_id': self.driver_id.id,
            # 'shipment_route': self.shipment_route,
            'arrived_date': self.arrived_date,
            'shipment_count':shipment_count,
        })
        # vals={
        #     'shipment_count':shipment_count,
        # }
        # print(vals)
        # self.env['stock.picking'].update(vals)


        # Close the wizard
        return {'type': 'ir.actions.act_window_close'}
