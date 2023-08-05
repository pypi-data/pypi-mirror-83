# Protean
from protean.core.aggregate import BaseAggregate
from protean.core.application_service import BaseApplicationService
from protean.core.command import BaseCommand
from protean.core.domain_event import BaseDomainEvent
from protean.core.field.basic import Integer, String
from protean.core.field.embedded import AggregateField
from protean.core.unit_of_work import UnitOfWork
from protean.globals import current_domain


class PersonCommand(BaseCommand):
    first_name = String(max_length=50, required=True)
    last_name = String(max_length=50, required=True)
    age = Integer(default=21)


class Person(BaseAggregate):
    first_name = String(max_length=50, required=True)
    last_name = String(max_length=50, required=True)
    age = Integer(default=21)

    @classmethod
    def add_newcomer(cls, person_dict):
        """Factory method to add a new Person to the system"""
        newcomer = Person(
            first_name=person_dict["first_name"],
            last_name=person_dict["last_name"],
            age=person_dict["age"],
        )

        # Publish Event via the domain
        current_domain.publish(PersonAdded(person=newcomer))

        return newcomer


class PersonAdded(BaseDomainEvent):
    person = AggregateField(Person)

    class Meta:
        aggregate_cls = Person


class PersonService(BaseApplicationService):
    @classmethod
    def add(cls, command: PersonCommand):
        with UnitOfWork():
            newcomer = Person.add_newcomer(command.to_dict())

            person_repo = current_domain.repository_for(Person)
            person_repo.add(newcomer)

        return newcomer
