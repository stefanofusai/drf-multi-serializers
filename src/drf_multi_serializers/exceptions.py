class ActionVersionSetError(Exception):
    """Raised when serializer_classes matches against both action and version."""

    def __init__(self) -> None:  # noqa: D107
        super().__init__("action and version can't be set at the same time")
