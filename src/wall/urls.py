from django.urls import path
from . import views


urlpatterns = [
    path('comment/', views.CommentsView.as_view({
        'post': 'create'
    }), name='wall_comment_create'),

    path('comment/<int:pk>/', views.CommentsView.as_view({
        'put': 'update',
        'delete': 'destroy'
    }), name='wall_comment_detail'),

    path('post/', views.PostView.as_view({
        'post': 'create'
    }), name='post_create'),

    path('post/<int:pk>/', views.PostView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='post_detail'),

    path('<int:pk>/', views.PostListView.as_view(), name='post_list'),
]
