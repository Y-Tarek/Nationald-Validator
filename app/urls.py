from django.urls import path
from .views import NationalIDAPI, ServiceTransactionAPI


urlpatterns = [
  
  path("nationalid/data/",NationalIDAPI.as_view(),name="nationalid-data"),
  path("service/transactions/",ServiceTransactionAPI.as_view(),name="service-trasnactions"),

]