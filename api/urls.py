from rest_framework.authtoken import views
from django.urls import include, path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from backend import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(urls)),
    path('auth/', views.obtain_auth_token)

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
