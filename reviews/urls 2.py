from django.urls import path
from .views import records_list

urlpatterns = [
    path('records/', records_list),
]