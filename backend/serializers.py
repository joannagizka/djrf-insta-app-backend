from django.contrib.auth.models import User, Group
from rest_framework import serializers

from backend.models import Photo


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo
        created = serializers.DateTimeField()
        fields = ['id', 'description', 'created', 'photo']


class UserSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, required=False)

    class Meta:
        model = User
        read_only = 'photos'
        fields = ['id', 'username', 'email', 'password', 'photos']
        extra_kwargs = {'password': {'required': True, 'write_only': True}}
        owner = serializers.ReadOnlyField(source='owner.username', read_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
