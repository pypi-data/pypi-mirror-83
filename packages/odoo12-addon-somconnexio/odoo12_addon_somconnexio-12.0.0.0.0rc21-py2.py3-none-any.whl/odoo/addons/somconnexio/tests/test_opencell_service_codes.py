from ..opencell_models.services import ServicesFromContract
from .factories import ContractFactory
from odoo.tests import TransactionCase


class TestOpenCellServiceCodes(TransactionCase):
    def setUp(self):
        self.contract = ContractFactory()
        self.expected_services = [{
            "code": "CODE",
            "quantity": 1,
            "subscriptionDate": (
                self.contract.contract_line_ids[0].date_start.strftime("%Y-%m-%d")
            ),
        }]

    def test_services_to_activate(self):
        services_from_contract = ServicesFromContract(
            self.contract
        ).services_to_activate()
        self.assertEquals(services_from_contract, self.expected_services)
