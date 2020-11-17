import datetime
import json

from django.http import HttpResponse
from django.template.backends import django
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.admin import User

from backend.models import Photo
from backend.serializers import UserSerializer, PhotoSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

   # permission_classes = [permissions.IsAuthenticated]

# class PhotoViewSet(viewsets.ModelViewSet):
#     queryset = Photo.objects.all()
#     serializer_class = PhotoSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


    def get_queryset(self):
        owner_queryset = self.queryset.filter(owner=self.request.user)
        return owner_queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        #created = datetime.now()
        Photo.objects.create(image=file, owner=request.auth.user)

        return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)



