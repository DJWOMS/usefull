from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>', views.FeedView.as_view({'get': 'retrieve'}), name='feed_detail'),
    path('', views.FeedView.as_view({'get': 'list'}), name='feed_list'),
]
