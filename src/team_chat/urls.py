from django.urls import path

from . import views

urlpatterns = [
    path('room/', views.RoomListView.as_view()),
    path('room/dialog/<str:room>/', views.DialogView.as_view())
]
