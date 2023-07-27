from rest_framework.viewsets import ModelViewSet
from .models import Video
from rest_framework import permissions
from rest_framework.decorators import action
from .serializers import VideoListSerializer, VideoDetailSerializer
from .permissions import IsAuthorOrAdmin
from rest_framework.response import Response
from impressions.serializers import CommentSerializer, LikedUserSerializer, FavoriteSerializer, RatedSerializer, \
    RatingSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from impressions.models import Like, Favorite, Rating


class StandartResultPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    pagination_class = StandartResultPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('title', 'description')
    filterset_fields = ('title', 'description')

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

    @action(methods=['POST', 'GET'], detail=True)
    def likes(self, request, pk):
        video = self.get_object()
        user = request.user
        if request.method == 'GET':
            likes = video.likes.all()
            serializer = LikedUserSerializer(instance=likes, many=True)
            return Response(serializer.data, status=200)

        elif request.method == 'POST':
            if user.likes.filter(video=video).exists():
                user.likes.filter(video=video).delete()
                return Response('Like was deleted', status=204)
            Like.objects.create(owner=user, video=video)
            return Response('Like has been added', status=201)

    @action(methods=['POST', 'GET'], detail=True)
    def favorites(self, request, pk):
        video = self.get_object()
        user = request.user
        if request.method == 'GET':
            favorites = video.favorites.all()
            serializer = FavoriteSerializer(instance=favorites, many=True)
            return Response(serializer.data, status=200)

        elif request.method == 'POST':
            if user.favorites.filter(video=video).exists():
                user.favorites.filter(video=video).delete()
                return Response('Video was deleted from favorites', status=204)
            Favorite.objects.create(owner=user, video=video)
            return Response('Video has been added to favorites', status=201)

    @action(methods=['GET', 'POST', 'PUT', 'DELETE'],detail =True)
    def rating(self, request, pk):
        video = self.get_object()
        user = request.user

        if request.method == 'GET':
            ratings = video.ratings.all()
            serializer = RatedSerializer(instance=ratings, many=True)
            return Response(serializer.data, status=200)

        elif request.method == 'POST':
            if user.ratings.filter(video=video).exists():
                return Response('You already rated this video')

            serializator = RatingSerializer(data=request.data, context={'video': video, 'owner': user})
            serializator.is_valid(raise_exception=True)
            serializator.save()
            return Response('Rating was added', status=201)

        elif request.method == 'PUT':
            user_rating = user.ratings.filter(video=video).first()
            if user_rating:
                serializer = RatedSerializer(user_rating, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=400)

        elif request.method == 'DELETE':
            if user.ratings.filter(video=video).exists():
                user.ratings.filter(video=video).delete()
                return Response('Rating was deleted', status=204)
        return Response({'error': 'Rating not found.'}, status=404)



