
from django.contrib import admin
from django.urls import path,include
from django.urls import re_path

urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('',include('HOUSE_ML.urls')),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
]
