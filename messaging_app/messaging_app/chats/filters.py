from django_filters import rest_framework as filters
from .models import Message
from django.utils import timezone
from datetime import timedelta
from .models import User


class MessageFilter(filters.FilterSet):
    user = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        field_name='sender',
        label='Sender'
    )

    start_date = filters.DateTimeFilter(
        field_name='sent_at',
        lookup_expr='gte',
        label='Start Date'
    )

    end_date = filters.DateTimeFilter(
        field_name='sent_at',
        lookup_expr='lte',
        label='End Date'
    )

    class Meta:
        model = Message
        fields = ['user', 'start_date', 'end_date']
