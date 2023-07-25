from rest_framework import serializers
from impressions.models import Rating, Comment
from .models import Video
from rest_framework.response import Response


class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    product = serializers.ReadOnlyField(source='video.title')

    class Meta:
        model = Rating
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    owner_email = serializers.ReadOnlyField(source='owner.email')
    video = serializers.ReadOnlyField(source='video.id')
    video_title = serializers.ReadOnlyField(source='video.title')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        video = self.context.get('file')
        video = Video.objects.get(file=video.file)
        owner = self.context.get('author')
        validated_data['owner'] = owner
        validated_data['video'] = video
        return super().create(validated_data)



