from django.contrib.auth.models import User
from rest_framework import serializers

from backend.models import Photo, Comment, Like, Observation


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='owner.username')
    isMe = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        created = serializers.DateTimeField()
        fields = ['photo', 'content', 'owner', 'created', 'username', 'isMe']
        read_only_fields = ['owner']

    def get_isMe(self, photo):
        return photo.owner == self.context['request'].user



class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    isLikedByMe = serializers.SerializerMethodField(read_only=True)
    likesAmount = serializers.SerializerMethodField(read_only=True)
    commentsAmount = serializers.SerializerMethodField(read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Photo
        created = serializers.DateTimeField()
        fields = ['id', 'description', 'created', 'photo', 'isLikedByMe', 'likesAmount', 'commentsAmount', 'owner']

    def get_isLikedByMe(self, photo):
        return Like.objects.filter(photo=photo, owner=self.context['request'].user).exists()

    def get_likesAmount(self, photo):
        return Like.objects.filter(photo=photo).count()

    def get_commentsAmount(self, photo):
        return Comment.objects.filter(photo=photo).count()


class SinglePhotoSerializer(serializers.HyperlinkedModelSerializer):
    comments = CommentSerializer(many=True, required=False)
    isLikedByMe = serializers.SerializerMethodField(read_only=True)
    likesAmount = serializers.SerializerMethodField(read_only=True)
    username = serializers.ReadOnlyField(source='owner.username')
    ownerId = serializers.ReadOnlyField(source='owner.id')
    isMe = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Photo
        created = serializers.DateTimeField()

        fields = ['id', 'description', 'created', 'photo', 'comments', 'isLikedByMe', 'likesAmount', 'username', 'isMe', 'ownerId']


    def get_isLikedByMe(self, photo):
        return Like.objects.filter(photo=photo, owner=self.context['request'].user).exists()

    def get_likesAmount(self, photo):
        return Like.objects.filter(photo=photo).count()

    def get_isMe(self, photo):
        return photo.owner == self.context['request'].user


class RegisteredUserSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, required=False)
    followersAmount = serializers.SerializerMethodField(read_only=True)
    followedByMe = serializers.SerializerMethodField(read_only=False)

    class Meta:
        model = User
        read_only_fields = ['photos']
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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

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

