from django.urls import path
from .views import NationalIDAPI


urlpatterns = [
  
  path("nationalid/data/",NationalIDAPI.as_view(),name="nationalid-data")
]