# Protean
from protean.utils import fully_qualified_name


class TestVORegistration:
    def test_auto_register_value_object_with_annotation(self, test_domain):
        # Protean
        from protean.core.field.basic import String

        @test_domain.aggregate
        class Foo:
            foo = String()

        @test_domain.value_object(aggregate_cls=Foo)
        class Bar:
            bar = String()

        assert fully_qualified_name(Bar) in test_domain.registry.value_objects
        assert Bar.meta_.aggregate_cls == Foo
