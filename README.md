# drf-multi-serializers

A simple package to handle multiple serializers for the same view in Django Rest Framework.

## Installation

```bash
pip install drf-multi-serializers
```

## Usage

Simply import the `MultiSerializerMixin` and use it in your API views:

```python
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet
from drf_multi_serializers import MultiSerializerMixin

...

class MyAPIView(MultiSerializerMixin, ListCreateAPIView):
    ...
    serializer_classes = {
        "create": MyCreateSerializer,
        "list": MyListSerializer,
    }
    ...

class MyViewSet(MultiSerializerMixin, ModelViewSet):
    ...
    serializer_classes = {
        "create": MyCreateSerializer,
        "list": MyListSerializer,
        "metadata": MyMetadataSerializer,  # create ViewSets require either serializer_class or metadata serializer for OPTION requests
        "partial_update": MyUpdateSerializer,
        "retrieve": MyRetrieveSerializer,
        "update": MyUpdateSerializer,
    }
    ...
```

## Contributing

Contributions are welcome! To get started, please refer to our [contribution guidelines](https://github.com/stefanofusai/drf-multi-serializers/blob/main/CONTRIBUTING.md).

## Issues

If you encounter any problems while using this package, please open a new issue [here](https://github.com/stefanofusai/drf-multi-serializers/issues).
