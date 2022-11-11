from rest_framework import mixins, viewsets
from rest_framework.pagination import PageNumberPagination


class MixedPermission:
    """ Permissions action`s mixin
    """

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class MixedSerializer:
    """ Serializer action`s mixin
    """

    def get_serializer(self, *args, **kwargs):
        try:
            serializer_class = self.serializer_classes_by_action[self.action]
        except KeyError:
            serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class MixedPermissionSerializer(MixedPermission, MixedSerializer):
    """ Permissions and serializer action`s mixin
    """
    pass


class RetrieveUpdateDestroy(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            MixedPermission,
                            viewsets.GenericViewSet):
    pass


class MixedPermissionViewSet(MixedPermission, viewsets.ViewSet):
    pass


class MixedPermissionGenericViewSet(MixedPermission, viewsets.GenericViewSet):
    pass


class CreateUpdateDestroy(mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          MixedPermission,
                          viewsets.GenericViewSet):
    """
    """
    pass


class CreateRetrieveUpdateDestroy(mixins.CreateModelMixin,
                                  mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin,
                                  MixedPermission,
                                  viewsets.GenericViewSet):
    """
    """
    pass


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000
