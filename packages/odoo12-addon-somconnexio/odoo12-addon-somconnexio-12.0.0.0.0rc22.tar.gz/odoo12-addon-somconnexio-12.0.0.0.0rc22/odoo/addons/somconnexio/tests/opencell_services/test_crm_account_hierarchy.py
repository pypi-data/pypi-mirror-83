from odoo.tests import TransactionCase
from mock import Mock, patch

from ...opencell_services.crm_account_hierarchy import \
    CRMAccountHierarchyFromContractService

from ..factories import ContractFactory


class OpenCellConfigurationFake:
    seller_code = 'SC'
    customer_category_code = 'CLIENT'


class CRMAccountHierarchyFromContractServiceTests(TransactionCase):

    def setUp(self):
        super().setUp()
        self.opencell_configuration = OpenCellConfigurationFake()

    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy.Access',  # noqa
        spec=['create']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy.AccessFromContract',  # noqa
        return_value=Mock(spec=['to_dict'])
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy.Subscription',  # noqa
        spec=['create']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy.SubscriptionFromContract',  # noqa
        return_value=Mock(spec=['to_dict'])
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy.CRMAccountHierarchy',  # noqa
        spec=['create']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy.CRMAccountHierarchyFromContract',  # noqa
        return_value=Mock(spec=['to_dict', 'code'])
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy.Customer',
        spec=['create']
    )
    @patch(
        'odoo.addons.somconnexio.opencell_services.crm_account_hierarchy.CustomerFromPartner',  # noqa
        return_value=Mock(spec=['to_dict'])
    )
    def test_run(
        self,
        MockCustomerFromPartner,
        MockCustomer,
        MockCRMAccountHierarchyFromContract,
        MockCRMAccountHierarchy,
        MockSubscriptionFromContract,
        MockSubscription,
        MockAccessFromContract,
            MockAccess):
        self.contract = ContractFactory()

        MockCustomerFromPartner.return_value.to_dict.return_value = {
            'example_data': 123
        }
        MockCRMAccountHierarchyFromContract.return_value.to_dict.return_value = {
            'example_data': 123
        }
        MockSubscriptionFromContract.return_value.to_dict.return_value = {
            'example_data': 123
        }
        MockAccessFromContract.return_value.to_dict.return_value = {
            'example_data': 123
        }

        CRMAccountHierarchyFromContractService(
            self.contract,
            self.opencell_configuration
        ).run()

        MockCustomerFromPartner.assert_called_with(
            self.contract.partner_id,
            self.opencell_configuration
        )
        MockCustomer.create.assert_called_with(
            **MockCustomerFromPartner.return_value.to_dict.return_value
        )
        MockCRMAccountHierarchyFromContract.assert_called_with(
            self.contract,
            self.contract.partner_id.id
        )
        MockCRMAccountHierarchy.create.assert_called_with(
            **MockCRMAccountHierarchyFromContract.return_value.to_dict.return_value
        )
        MockSubscriptionFromContract.assert_called_with(
            self.contract,
            MockCRMAccountHierarchyFromContract.return_value.code
        )
        MockSubscription.create.assert_called_with(
            **MockSubscriptionFromContract.return_value.to_dict.return_value
        )
        MockAccessFromContract.assert_called_with(
            self.contract
        )
        MockAccess.create.assert_called_with(
            **MockAccessFromContract.return_value.to_dict.return_value
        )
