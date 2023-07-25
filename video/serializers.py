from rest_framework import serializers
from .models import Video
from impressions.serializers import CommentSerializer


class VideoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['author', 'title', 'created_at']


class VideoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

    def to_representation(self, instance):
        data = super(VideoDetailSerializer, self).to_representation(instance)
        data['comments_count'] = instance.comments.count()
        data['comments'] = CommentSerializer(instance.comments.all(), many=True, required=False).data
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        video = Video.objects.create(author=request.user, **validated_data)
        return video
