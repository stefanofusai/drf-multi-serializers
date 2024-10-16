from rest_framework.serializers import Serializer

from .exceptions import ActionVersionSetError


class MultiSerializerMixin:
    """A mixin that allows you to define different serializers for different view actions/methods/versions."""

    serializer_classes: dict[str, type[Serializer] | dict[str, type[Serializer]]]

    def get_serializer_class(self) -> type[Serializer]:  # noqa: D102
        action = getattr(self, "action", None)
        version = self.request.version

        if action in self.serializer_classes and version in self.serializer_classes:
            raise ActionVersionSetError

        if action is not None and action in self.serializer_classes:
            action_serializer_or_versioned_serializers = self.serializer_classes[action]

            if (
                isinstance(action_serializer_or_versioned_serializers, dict)
                and version is not None
                and version in action_serializer_or_versioned_serializers
            ):
                return action_serializer_or_versioned_serializers[version]

            if issubclass(action_serializer_or_versioned_serializers, Serializer):
                return action_serializer_or_versioned_serializers

        if version is not None and version in self.serializer_classes:
            return self.serializer_classes[version]

        return super().get_serializer_class()
