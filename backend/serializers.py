from django.contrib.auth.models import User, Group
from rest_framework import serializers

from backend.models import Photo


class UserSerializer(serializers.HyperlinkedModelSerializer):
    photo = serializers.PrimaryKeyRelatedField(many=True, queryset=Photo.objects.all())

    class Meta:
        model = User
        read_only = 'photo'
        fields = ['id', 'username', 'email', 'password', 'photos']
        read_only_fields = ['photos']
        extra_kwargs = {'password': {'required': True, 'write_only': True}}
        owner = serializers.ReadOnlyField(source='owner.username', read_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo
        created = serializers.DateTimeField()
        fields = ['description', 'created', 'photo']
