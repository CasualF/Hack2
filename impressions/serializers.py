from rest_framework import serializers
from impressions.models import Rating, Comment, Like, Favorite
from video.models import Video
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


class CommentListSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')

    class Meta:
        model = Comment
        fields = ['owner_email', 'content', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        video = attrs['video']
        if user.likes.filter(video=video).exists():
            return Response('You already liked this video', status=400)
        return attrs


class LikedUserSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    video_title = serializers.ReadOnlyField(source='video.title')

    class Meta:
        model = Like
        fields = ('owner_email', 'video_title')


class FavoriteSerializer(serializers.ModelSerializer):
    owner_email = serializers.ReadOnlyField(source='owner.email')
    video_title = serializers.ReadOnlyField(source='video.title')

    class Meta:
        model = Favorite
        fields = ['owner_email', 'video_title']
