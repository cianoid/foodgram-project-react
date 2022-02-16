from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('secure_zone/', admin.site.urls),
]
