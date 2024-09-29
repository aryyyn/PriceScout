from django.urls import path
from .views import *
urlpatterns = [
    path('home/', DataExtract, name="data extract")
]
