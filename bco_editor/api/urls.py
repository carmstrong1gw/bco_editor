from django.urls import path
from .views import BcoViewAll, BcoGetObject, BcoPostObject

urlpatterns = [
    path('bco/objects/view/all/', BcoViewAll.as_view()),
    path('bco/objects/view/<str:object_id>/', BcoGetObject.as_view()),
    path('bco/objects/create/', BcoPostObject.as_view()),
    path('<str:object_id>', BcoGetObject.as_view())
]
