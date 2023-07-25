from rest_framework import serializers

from impressions.models import Rating


class RatingSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    product = serializers.ReadOnlyField(source='video.title')

    class Meta:
        model = Rating
        fields = '__all__'
