from rest_framework.serializers import Serializer


class MultiSerializerMixin:
    """A mixin that allows you to define different serializers for different ViewSet actions."""  # noqa: E501

    serializer_classes: dict[str, type[Serializer]]

    def get_serializer_class(self) -> type[Serializer]:  # noqa: D102
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]

        return super().get_serializer_class()
