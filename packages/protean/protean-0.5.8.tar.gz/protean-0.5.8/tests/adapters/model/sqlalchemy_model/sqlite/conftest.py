# Standard Library Imports
import os

# Protean
import pytest


def initialize_domain():
    # Protean
    from protean.domain import Domain

    domain = Domain("SQLAlchemy Test - SQLite")

    # Construct relative path to config file
    current_path = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(current_path, "./config.py")

    if os.path.exists(config_path):
        domain.config.from_pyfile(config_path)

    return domain


domain = initialize_domain()


@pytest.fixture(autouse=True)
def test_domain():
    with domain.domain_context():
        yield domain


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    with domain.domain_context():
        # Create all associated tables
        # Local/Relative Imports
        from .elements import ComplexUser, Person, Provider, ProviderCustomModel, User
        from .test_array_datatype import ArrayUser, IntegerArrayUser
        from .test_json_datatype import Event

        domain.register(ArrayUser)
        domain.register(ComplexUser)
        domain.register(Event)
        domain.register(IntegerArrayUser)
        domain.register(Person)
        domain.register(Provider)
        domain.register(User)
        domain.register_model(ProviderCustomModel, entity_cls=Provider)

        domain.get_dao(ArrayUser)
        domain.get_dao(ComplexUser)
        domain.get_dao(Event)
        domain.get_dao(IntegerArrayUser)
        domain.get_dao(Person)
        domain.get_dao(Provider)
        domain.get_dao(User)

        for provider in domain.providers_list():
            provider._metadata.create_all()

        yield

        # Drop all tables at the end of test suite
        for provider in domain.providers_list():
            provider._metadata.drop_all()


@pytest.fixture(autouse=True)
def run_around_tests(test_domain):
    yield
    if test_domain.providers.has_provider("default"):
        test_domain.get_provider("default")._data_reset()
