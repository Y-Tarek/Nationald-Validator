from django.urls import path
from .views import CountryCodeAPI, RegisterServiceAPI, NationalIDAPI


urlpatterns = [
  path("country/code/",CountryCodeAPI.as_view(),name="list-country-code"),
  path("service/register/",RegisterServiceAPI.as_view(),name="service-register"),
  path("nationalid/data/",NationalIDAPI.as_view(),name="nationalid-data")
]