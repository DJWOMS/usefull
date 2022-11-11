from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.RoomView.as_view({'get': 'list', 'post': 'create_room'})),
    path('rooms/team/', views.RoomView.as_view({'post': 'create_team_room'})),
    path('dialog/', views.DialogView.as_view()),
    path('dialog/<int:pk>/', views.DialogView.as_view()),

    path('room/', views.index),
    path('room/<int:pk>/', views.room),
]
