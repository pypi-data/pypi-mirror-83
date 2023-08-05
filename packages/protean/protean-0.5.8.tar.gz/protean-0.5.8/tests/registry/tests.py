# Standard Library Imports
from datetime import datetime
from enum import Enum

# Protean
import inflection
import pytest

from protean.core.aggregate import BaseAggregate
from protean.core.field.basic import DateTime, String
from protean.domain.registry import _DomainRegistry
from protean.utils import DomainObjects


class Role(BaseAggregate):
    name = String(max_length=15, required=True)
    created_on = DateTime(default=datetime.today())


def test_element_registration():
    register = _DomainRegistry()
    register.register_element(Role)

    assert (
        "tests.registry.tests.Role" in register._elements[DomainObjects.AGGREGATE.value]
    )


def test_delisting_element():
    register = _DomainRegistry()
    register.register_element(Role)

    assert (
        "tests.registry.tests.Role" in register._elements[DomainObjects.AGGREGATE.value]
    )

    register.delist_element(Role)

    assert (
        "tests.registry.tests.Role"
        not in register._elements[DomainObjects.AGGREGATE.value]
    )


def test_fetching_elements_from_registry():
    register = _DomainRegistry()
    register.register_element(Role)

    aggregates = register.get(DomainObjects.AGGREGATE)
    assert "tests.registry.tests.Role" in aggregates


def test_that_registry_exposes_properties():
    # Assert that lowercased, underscored, pluralized methods
    # are attached to registry for each element type
    assert all(
        inflection.pluralize(inflection.underscore(element_type.value.lower()))
        for element_type in DomainObjects
    )


def test_that_registering_an_unknown_element_type_triggers_an_error():
    class DummyEnum(Enum):
        UNKNOWN = "UNKNOWN"

    class FooBar1:
        element_type = "FOOBAR"

    class FooBar2:
        element_type = DummyEnum.UNKNOWN

    class FooBar3:
        pass

    register = _DomainRegistry()

    with pytest.raises(NotImplementedError):
        register.register_element(FooBar1)

    with pytest.raises(NotImplementedError):
        register.register_element(FooBar2)

    with pytest.raises(NotImplementedError):
        register.register_element(FooBar3)


def test_that_delisting_an_unknown_element_type_triggers_an_error():
    class DummyEnum(Enum):
        UNKNOWN = "UNKNOWN"

    class FooBar1:
        element_type = "FOOBAR"

    class FooBar2:
        element_type = DummyEnum.UNKNOWN

    class FooBar3:
        pass

    register = _DomainRegistry()

    with pytest.raises(NotImplementedError):
        register.delist_element(FooBar1)

    with pytest.raises(NotImplementedError):
        register.delist_element(FooBar2)

    with pytest.raises(NotImplementedError):
        register.delist_element(FooBar3)


def test_that_re_registering_an_element_has_no_effect():
    register = _DomainRegistry()
    register.register_element(Role)
    register.register_element(Role)

    assert len(register._elements[DomainObjects.AGGREGATE.value]) == 1
    assert (
        "tests.registry.tests.Role" in register._elements[DomainObjects.AGGREGATE.value]
    )
