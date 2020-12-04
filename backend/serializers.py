from django.contrib.auth.models import User
from rest_framework import serializers

from backend.models import Photo, Comment, Like, Observation


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
    followersAmount = serializers.SerializerMethodField(read_only=True)
    followedByMe = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        read_only_fields = ['photos', 'followedByMe']
        fields = ['id', 'username', 'email', 'password', 'photos', 'followersAmount', 'followedByMe']
        extra_kwargs = {'password': {'required': True, 'write_only': True}}
        owner = serializers.ReadOnlyField(source='owner.username', read_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def get_followedByMe(self, user):
        return Observation.objects.filter(follower=self.context['request'].user, following=user).exists()

    def get_followersAmount(self, user):
        return Observation.objects.filter(following=user).count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['photo', 'owner']
        read_only_fields = ['owner', 'photo']


class ObservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observation
        fields = ['follower', 'following']
        read_only_fields = ['follower', 'following']
