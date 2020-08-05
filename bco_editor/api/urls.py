from django.urls import path
from .views import BcoAPIView

urlpatterns = [
    path('bco/', BcoAPIView.as_view()),
]
