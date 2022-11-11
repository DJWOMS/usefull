from django.urls import path
from . import views

urlpatterns = [
    path('faq/', views.FaqListView.as_view()),
    path('guide/', views.GuideListView.as_view()),
    path('guide/<int:pk>/', views.GuideView.as_view()),
    path('category/', views.CategoryListView.as_view(), name='support_category_list'),
    path('ticket/', views.TicketView.as_view(), name='ticket_create'),
    path('', views.TicketListView.as_view(), name='ticket_list'),
]
