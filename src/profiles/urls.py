from django.urls import path
from . import views

urlpatterns = [
    path('scheme/', views.ColorSchemaView.as_view({'get': 'retrieve', 'put': 'update'})),

    path('list/', views.ProfileListView.as_view(), name='profile_list'),
    path('avatar/', views.ProfileAvatarView.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='update_avatar'
    ),
    path('<int:pk>/', views.ProfilePublicView.as_view({'get': 'retrieve'}),
         name='profile_public_detail'
         ),

    path('progress/', views.ProgressView.as_view(), name='progress'),
    path('technology/', views.TechnologyListView.as_view(), name='technology_list'),
    path('technology/<int:id>/', views.TechnologyDeleteView.as_view(), name='technology_delete'),
    path('', views.ProfilePrivateView.as_view(), name='profile_private_detail'),
]
