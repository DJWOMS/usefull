from django.urls import path
from . import views


urlpatterns = [
    path('list/', views.FollowerListView.as_view(), name='follower_list'),
    path('following/', views.FollowingView.as_view(), name='following'),
    path('<int:pk>/', views.FollowerView.as_view(), name='following_delete'),
    path('', views.FollowerView.as_view(), name='follower_detail'),

]
