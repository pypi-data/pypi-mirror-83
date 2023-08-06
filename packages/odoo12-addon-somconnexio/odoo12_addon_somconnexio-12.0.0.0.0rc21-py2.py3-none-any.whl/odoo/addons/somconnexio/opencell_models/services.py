from .opencell_resource import OpenCellResource


class ServicesFromContract(OpenCellResource):
    def __init__(self, contract):
        self.contract = contract

    def services_to_activate(self):
        """
        Return a list of dicts with the OpenCell service code
        and the start date of the contract line.

        To construct the dict, you need to get the service code
        form the product and the date from the
        start date of the contract line.

        :return array: List of dictionaries with the code and the start date.
        """
        services = []
        for line in self.contract.contract_line_ids:
            opencell_service_dict = ContractLineToOCServiceDict(line).convert()
            services.append(opencell_service_dict)
        return services


class ContractLineToOCServiceDict:
    """
    Presenter parsing OpenCell service and
    returning an OpenCell compliant service
    """

    def __init__(self, contract_line):
        self.contract_line = contract_line

    @staticmethod
    def service_dict(service_code, subscription_date):
        return {
            "code": service_code,
            "quantity": 1,
            "subscriptionDate": subscription_date,
        }

    def convert(self):
        return self.service_dict(
            self.contract_line.product_id.default_code,
            self.contract_line.date_start.strftime("%Y-%m-%d")
        )
