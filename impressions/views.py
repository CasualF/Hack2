from rest_framework import permissions, generics
from video.models import Video
from video.serializers import VideoDetailSerializer
from django.db.models import Avg


class RecommendationView(generics.ListAPIView):
    queryset = Video.objects.annotate(average_rating = Avg('ratings__rating')).order_by('-average_rating')
    serializer_class = VideoDetailSerializer
    permission_classes = permissions.AllowAny,
