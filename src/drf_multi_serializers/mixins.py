from typing import Any

from rest_framework.request import Request
from rest_framework.serializers import Serializer

from .exceptions import ActionVersionSetError


class MultiSerializerMixin:
    """A mixin that allows you to define different serializers for different view actions/methods/versions."""

    request: Request
    serializer_classes: dict[
        str, type[Serializer[Any]] | dict[str, type[Serializer[Any]]]
    ]

    def get_serializer_class(self) -> type[Serializer[Any]]:
        """
        Get the appropriate serializer class based on the view's action or the request's version.

        :raises ActionVersionSetError: If both action and version are set in `serializer_classes`
        :raises TypeError: If the `serializer_classes` dictionary contains values of invalid type
        :raises NotImplementedError: If the parent class does not implement `get_serializer_class`
        :return: The appropriate serializer class
        :rtype: type[Serializer]
        """
        parent = super()

        if not hasattr(parent, "get_serializer_class"):
            msg = "get_serializer_class not implemented in parent class"
            raise NotImplementedError(msg)

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

            if isinstance(
                action_serializer_or_versioned_serializers, type
            ) and issubclass(action_serializer_or_versioned_serializers, Serializer):
                return action_serializer_or_versioned_serializers

            msg = f"Invalid type for serializer_classes['{action}']: {type(action_serializer_or_versioned_serializers)}. Expected a Serializer class or a dict mapping version strings to Serializer classes"
            raise TypeError(msg)

        if version is not None and version in self.serializer_classes:
            versioned_serializer = self.serializer_classes[version]

            if isinstance(versioned_serializer, type) and issubclass(
                versioned_serializer, Serializer
            ):
                return versioned_serializer

            msg = f"Invalid type for serializer_classes['{version}']: {type(versioned_serializer)}. Expected a Serializer class"
            raise TypeError(msg)

        return parent.get_serializer_class()  # type: ignore[no-any-return]
