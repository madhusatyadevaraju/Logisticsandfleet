{
    'name' : 'Logistics And Fleet Management System',
    'author' : 'Ben Franklin',
    'version' :'17.0.0.0',
    'license' :'LGPL-3',
    'summary' :'Manage fleet,routes,drivers and shipments',
    'category':'logistics',
    'depends': ['fleet','sale','stock'],
    'data':[
        'security/ir.model.access.csv',
        'views/transport_location_views.xml',
        'views/transporters_views.xml',
        'views/transport_routes_views.xml',
        'views/shipment_type_views.xml',
        'views/vehicles_views.xml',
        'views/sale_order_views.xml',
        'wizard/shipment_details_wizard_views.xml',
        'views/stock_picking_views.xml',
        'views/transport_entry_views.xml',
        'views/menu.xml',

    ],

}