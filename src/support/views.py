from rest_framework import generics, permissions

from src.support.models import Ticket, Category, Faq, Guide
from src.support import serializers


class FaqListView(generics.ListAPIView):
    """ FAQ list view"""
    queryset = Faq.objects.all()
    serializer_class = serializers.FaqListSerializer
    permission_classes = [permissions.AllowAny]


class GuideListView(generics.ListAPIView):
    """ Guide list view"""
    queryset = Guide.objects.all()
    serializer_class = serializers.GuideListSerializer
    permission_classes = [permissions.AllowAny]


class GuideView(generics.RetrieveAPIView):
    """ Guide view"""
    queryset = Guide.objects.all()
    serializer_class = serializers.GuideSerializer
    permission_classes = [permissions.AllowAny]


class CategoryListView(generics.ListAPIView):
    """ Ticket category list view"""
    queryset = Category.objects.all()
    serializer_class = serializers.SupportCategoryListSerializer
    permission_classes = [permissions.IsAuthenticated]


class TicketListView(generics.ListAPIView):
    """ Ticket list view"""
    serializer_class = serializers.TicketListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user__id=self.request.user.id)


class TicketView(generics.CreateAPIView):
    """ Ticket detail view"""
    serializer_class = serializers.TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
