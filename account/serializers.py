from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)
    password_confirmation = serializers.CharField(min_length=6, max_length=20, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirmation', 'first_name', 'last_name', 'avatar')

    def validate(self, attrs):
        password = attrs['password']
        password_confirmation = attrs.pop('password_confirmation')

        if password != password_confirmation:
            raise serializers.ValidationError('Passwords do not match')

        if password.isdigit() or password.isalpha():
            raise serializers.ValidationError('Password must contain letters and numbers')

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ActivationSerializer(serializers.Serializer):
    activation_code = serializers.CharField(required=True)

    def validate(self, attrs):
        self.activation_code = attrs['activation_code']
        return attrs

    def save(self, **kwargs):
        try:
            user = User.objects.get(activation_code=self.activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
        except:
            self.fail('Incorrect activation code')
