from rest_framework import serializers
from .models import Video
from impressions.serializers import CommentListSerializer, FavoriteSerializer, LikedUserSerializer


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
        data['like_count'] = instance.likes.count()
        data['likes'] = LikedUserSerializer(instance.likes.all(), many=True, required=False).data
        data['favorite_count'] = instance.favorites.count()
        data['favorites'] = FavoriteSerializer(instance.favorites.all(), many=True, required=False).data
        data['comments_count'] = instance.comments.count()
        data['comments'] = CommentListSerializer(instance.comments.all(), many=True, required=False).data

        user = self.context['request'].user
        if user.is_authenticated:
            data['is_liked'] = self.is_liked(instance, user)
            data['is_favorite'] = self.is_favorite(instance, user)
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        video = Video.objects.create(author=request.user, **validated_data)
        return video

    @staticmethod
    def is_liked(video, user):
        return user.likes.filter(video=video).exists()

    @staticmethod
    def is_favorite(video, user):
        return user.favorites.filter(video=video).exists()
