from django.urls import path
from .views import DEBUG, BcoPostObject, BcoGetObject, BcoPatchObject, BcoDeleteObject, BcoGetAll

urlpatterns = [
    path('debug/', DEBUG.as_view()),
    path('bco/objects/create/', BcoPostObject.as_view()),
    path('bco/objects/read/', BcoGetObject.as_view()),
    path('bco/objects/update/', BcoPatchObject.as_view()),
    path('bco/objects/delete/', BcoDeleteObject.as_view()),
    path('bco/objects/read/all/', BcoGetAll.as_view()),
    path('bco/objects/read/<str:object_id>/', BcoGetObject.as_view()),
    path('<str:object_id>', BcoGetObject.as_view())
]
