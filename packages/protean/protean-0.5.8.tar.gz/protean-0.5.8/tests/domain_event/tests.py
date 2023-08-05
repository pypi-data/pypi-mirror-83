# Protean
import pytest

from mock import patch
from protean.adapters.broker.inline import InlineBroker
from protean.core.domain_event import BaseDomainEvent
from protean.globals import current_domain
from protean.infra.event_log import EventLog, EventLogRepository
from protean.utils import fully_qualified_name

# Local/Relative Imports
from .elements import Person, PersonAdded, PersonCommand, PersonService


class TestDomainEventInitialization:
    def test_that_base_domain_event_class_cannot_be_instantiated(self):
        with pytest.raises(TypeError):
            BaseDomainEvent()

    def test_that_domain_event_can_be_instantiated(self):
        service = PersonAdded()
        assert service is not None


class TestDomainEventRegistration:
    def test_that_domain_event_can_be_registered_with_domain(self, test_domain):
        test_domain.register(PersonAdded)

        assert fully_qualified_name(PersonAdded) in test_domain.registry.domain_events

    def test_that_domain_event_can_be_registered_via_annotations(self, test_domain):
        @test_domain.domain_event(aggregate_cls=Person)
        class AnnotatedDomainEvent:
            def special_method(self):
                pass

        assert (
            fully_qualified_name(AnnotatedDomainEvent)
            in test_domain.registry.domain_events
        )


class TestDomainEventTriggering:
    @patch.object(InlineBroker, "send_message")
    def test_that_domain_event_is_raised_in_aggregate_command_method(self, mock):
        newcomer = Person.add_newcomer(
            {"first_name": "John", "last_name": "Doe", "age": 21}
        )
        mock.assert_called_once_with(PersonAdded(person=newcomer))

    def test_that_domain_event_is_persisted(self, test_domain):
        test_domain.register(Person)
        test_domain.register(EventLog)
        test_domain.register(EventLogRepository)

        command = PersonCommand(first_name="John", last_name="Doe", age=21)
        person = PersonService.add(command)

        event_repo = current_domain.repository_for(EventLog)
        event = event_repo.get_most_recent_event_by_type(kind=PersonAdded)

        assert event is not None
        assert event.kind == "PersonAdded"
        assert event.payload["person"] == person.to_dict()

    def test_that_all_domain_events_are_retrievable(self, test_domain):
        test_domain.register(Person)
        test_domain.register(EventLog)
        test_domain.register(EventLogRepository)

        command = PersonCommand(first_name="John", last_name="Doe", age=21)
        person = PersonService.add(command)

        event_repo = current_domain.repository_for(EventLog)
        events = event_repo.get_all_events_of_type(kind=PersonAdded)

        assert events is not None
        assert isinstance(events, list)
        assert len(events) == 1
        assert events[0].kind == "PersonAdded"
        assert events[0].payload["person"] == person.to_dict()
