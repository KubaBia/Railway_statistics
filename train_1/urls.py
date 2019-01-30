
from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", homeView.as_view()),
    path("test.py/", testpy.as_view()),
    path("connection/<slug:id>", connectionView.as_view()),
    path("1",test1.as_view()),
]
