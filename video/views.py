from rest_framework.viewsets import ModelViewSet
from .models import Video
from rest_framework import permissions
from rest_framework.decorators import action
from .serializers import VideoListSerializer, VideoDetailSerializer
from .permissions import IsAuthorOrAdmin
from rest_framework.response import Response
from impressions.serializers import CommentSerializer


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list']:
            return VideoListSerializer
        return VideoDetailSerializer

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            return IsAuthorOrAdmin(),
        return permissions.IsAuthenticatedOrReadOnly(),

    @action(methods=['GET', 'POST', 'DELETE'], detail=True)
    def comments(self, request, pk):
        video = self.get_object()
        user = request.user
        if request.method == 'GET':
            comments = video.comments.all()
            serializer = CommentSerializer(instance=comments, many=True)
            return Response(serializer.data, status=200)

        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data, context={'file': video, 'author': user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=201)

        elif request.method == 'DELETE':
            comment_id = self.request.query_params.get('id')
            comment = video.comments.filter(video=video, pk=comment_id)
            print(dir(comment))
            if comment.exists():
                comment.delete()
                return Response('Successfully deleted', status=204)
        return Response('Not found', status=404)