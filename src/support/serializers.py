from rest_framework import serializers

from src.support.models import Ticket, Category, Faq, Guide


class SupportCategoryListSerializer(serializers.ModelSerializer):
    """ Category list serializer """

    class Meta:
        model = Category
        fields = ('id', 'name')


class TicketListSerializer(serializers.ModelSerializer):
    """ Ticket list serializer """
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Ticket
        fields = ('id', 'category', 'title', 'status')


class TicketSerializer(serializers.ModelSerializer):
    """ Ticket detail serializer """

    class Meta:
        model = Ticket
        fields = ('category', 'title', 'text', 'image')


class FaqListSerializer(serializers.ModelSerializer):
    """ Faq list serializer """

    class Meta:
        model = Faq
        fields = ('id', 'question', 'answer', 'most')


class GuideListSerializer(serializers.ModelSerializer):
    """ Guide list serializer """

    class Meta:
        model = Guide
        fields = ('id', 'title')


class GuideSerializer(serializers.ModelSerializer):
    """ Guide detail serializer """

    class Meta:
        model = Guide
        fields = ('id', 'title', 'content')
