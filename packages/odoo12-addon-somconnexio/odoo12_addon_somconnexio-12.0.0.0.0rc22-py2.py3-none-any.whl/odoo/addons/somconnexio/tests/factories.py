import factory
from factory import fuzzy
import datetime
factory.Faker._DEFAULT_LOCALE = 'es_ES'


class OdooModel(object):
    """ Represents Tryton's model """

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class OdooModelFactory(factory.Factory):
    """ Generates Tryton's model instances """

    class Meta:
        abstract = True
        model = OdooModel
        strategy = 'build'

    id = factory.Sequence(lambda n: n)

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        return target_class(*args, **kwargs)


class CountryFactory(OdooModelFactory):
    name = factory.Faker("country")
    code = factory.Faker("country_code")


class StateFactory(OdooModelFactory):
    name = factory.Faker("state")


class PartnerFactory(OdooModelFactory):
    street = factory.Faker("street_address")
    street2 = factory.Faker("secondary_address")
    zip = factory.Faker("postcode")
    city = factory.Faker("city")
    state_id = factory.SubFactory(StateFactory)
    country_id = factory.SubFactory(CountryFactory)

    @property
    def full_street(self):
        return "{} {}".format(self.street, self.street2)


class OpenCellConfigurationFactory(OdooModelFactory):
    customer_category_code = 'CLIENT'
    seller_code = 'SC'


class ProductFactory(OdooModelFactory):
    default_code = "CODE"


class ContractLineFactory(OdooModelFactory):
    product_id = factory.SubFactory(ProductFactory)
    date_start = fuzzy.FuzzyDate(datetime.date(2008, 1, 1))


class ContractFactory(OdooModelFactory):
    contract_line_ids = factory.List([ContractLineFactory()])
    partner_id = factory.SubFactory(PartnerFactory)
