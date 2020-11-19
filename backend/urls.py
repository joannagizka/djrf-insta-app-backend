from django.urls import include, path
from rest_framework import routers

from backend import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'photo', views.PhotoViewSet)
router.register(r'allphotos', views.AllPhotosViewSet)
router.register(r'myprofilephotos', views.MyProfilePhotosViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
