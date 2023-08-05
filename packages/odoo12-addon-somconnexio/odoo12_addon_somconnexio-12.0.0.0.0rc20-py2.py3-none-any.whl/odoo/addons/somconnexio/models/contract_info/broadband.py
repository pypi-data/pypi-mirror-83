from odoo import models, fields


class BroadbandServiceContractInfo(models.AbstractModel):
    _name = 'broadband.service.contract.info'
    _inherit = 'base.service.contract.info'
    ppp_user = fields.Char('PPP User')
    ppp_password = fields.Char('PPP Password')
    endpoint_user = fields.Char('Endpoint User')
    endpoint_password = fields.Char('Endpoint Password')


class VodafoneFiberServiceContractInfo(models.Model):
    _name = 'vodafone.fiber.service.contract.info'
    _inherit = 'base.service.contract.info'
    vodafone_id = fields.Char('Vodafone ID', required=True)
    vodafone_offer_code = fields.Char('Vodafone Offer Code', required=True)


class OrangeFiberServiceContractInfo(models.Model):
    _name = 'orange.fiber.service.contract.info'
    _inherit = 'broadband.service.contract.info'
    orange_id = fields.Char('Orange ID', required=True)


class OrangeADSLServiceContractInfo(models.Model):
    _name = 'orange.adsl.service.contract.info'
    _inherit = 'broadband.service.contract.info'
    administrative_number = fields.Char('Administrative Number', required=True)
    router_product_id = fields.Many2one(
        'product.product', 'Router Model', required=True
    )
    router_lot_id = fields.Many2one(
        'stock.production.lot', 'S/N / MAC Address', required=True
    )
    ppp_user = fields.Char(required=True)
    ppp_password = fields.Char(required=True)
    endpoint_user = fields.Char(required=True)
    endpoint_password = fields.Char(required=True)
