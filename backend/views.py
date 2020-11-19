import json
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.admin import User
from rest_framework.response import Response
from backend.models import Photo
from backend.serializers import UserSerializer, PhotoSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        owner_queryset = self.queryset.filter(owner=self.request.user)
        return owner_queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        Photo.objects.create(image=file, owner=request.auth.user)

        return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)


class AllPhotosViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = PhotoSerializer(queryset, many=True)
        return Response(serializer.data)


class CurrentUserViewSet(viewsets.ModelViewSet):
    model = User
    serializer_class = UserSerializer

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('pk') == 'current' and request.user:
            kwargs['pk'] = request.user.pk

        return super(CurrentUserViewSet, self).dispatch(request, *args, **kwargs)


class MyProfilePhotosViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_queryset(self):
        owner_queryset = self.queryset.filter(owner=self.request.user)
        return owner_queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = PhotoSerializer(queryset, many=True)
        return Response(serializer.data)
