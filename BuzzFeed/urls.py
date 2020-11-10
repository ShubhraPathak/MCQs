from django.contrib import admin
from django.urls import path, include
from .router import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('quiz.urls')),
    path('nested_admin', include('nested_admin.urls')),
    path('api/',include(router.urls))
]
