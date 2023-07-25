from rest_framework.viewsets import ModelViewSet
from .models import Video
from rest_framework import permissions
from rest_framework.decorators import action
from .serializers import VideoListSerializer, VideoDetailSerializer
from .permissions import IsAuthorOrAdmin


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return VideoListSerializer
        return VideoDetailSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            return IsAuthorOrAdmin(),
        return permissions.IsAuthenticatedOrReadOnly(),

