from django.urls import include, path
from rest_framework import routers

from backend import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'photo', views.PhotoViewSet, basename='photo')
router.register(r'allphotos', views.AllPhotosViewSet, basename='allphotos')
router.register(r'myprofilephotos', views.MyProfilePhotosViewSet, basename='myprofilephotos')
router.register(r'comments', views.CommentViewSet, basename='comments')
router.register(r'photodetails', views.PhotoDetailsViewSet, basename='photodetails')

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
