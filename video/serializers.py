from rest_framework import serializers
from .models import Video


class VideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['author', 'title', 'created_at']


class VideoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'
