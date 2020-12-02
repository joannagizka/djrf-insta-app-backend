from django.contrib.auth.models import User
from rest_framework import serializers

from backend.models import Photo, Comment, Like


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        created = serializers.DateTimeField()
        fields = ['photo', 'content', 'owner', 'created']
        read_only_fields = ['owner']


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Photo
        created = serializers.DateTimeField()
        fields = ['id', 'description', 'created', 'photo']


class SinglePhotoSerializer(serializers.HyperlinkedModelSerializer):
    comments = CommentSerializer(many=True, required=False)
    isLikedByMe = serializers.SerializerMethodField(read_only=True)
    likesAmount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Photo
        created = serializers.DateTimeField()

        fields = ['id', 'description', 'created', 'photo', 'comments', 'isLikedByMe', 'likesAmount']

    def get_isLikedByMe(self, photo):
        return Like.objects.filter(photo=photo, owner=self.context['request'].user).exists()

    def get_likesAmount(self, photo):
        return Like.objects.filter(photo=photo).count()





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


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['photo', 'owner']
        read_only_fields = ['owner', 'photo']
