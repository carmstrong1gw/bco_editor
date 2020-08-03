from django.urls import path
from .views import Bco27912020APIView

urlpatterns = [
    path('bco27912020/', Bco27912020APIView.as_view()),
]
