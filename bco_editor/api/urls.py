from django.urls import path
from .views import BcoViewAll, BcoViewObject, BcoCreateObject

urlpatterns = [
    path('bco/objects/view/all/', BcoViewAll.as_view()),
    path('bco/objects/view/<str:object_id>/', BcoViewObject.as_view()),
    path('bco/objects/create/', BcoCreateObject.as_view()),
    path('<str:object_id>', BcoViewObject.as_view())
]
