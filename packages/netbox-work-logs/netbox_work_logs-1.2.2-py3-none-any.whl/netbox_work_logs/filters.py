import django_filters
from django.contrib.auth.models import User
from django.db.models import Q

from utilities.filters import BaseFilterSet
from .models import Category, VMWorkLog, DeviceWorkLog

class DeviceWorkLogFilterSet(BaseFilterSet):
    """
    Device Work Log Filter Set
    """
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    time = django_filters.DateTimeFromToRangeFilter()
    user = django_filters.ModelMultipleChoiceFilter(
        field_name='user__id',
        queryset=User.objects.all(),
        to_field_name='id',
        label='Author',
    )
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='category__id',
        queryset=Category.objects.all(),
        to_field_name='id',
        label='Category',
    )

    class Meta:
        model = DeviceWorkLog
        fields = [
            'id', 'category', 'subject', 'user', 'content', 'internal_only', 'log_id', 'ticket_id', 'time'
        ]
    
    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(category__category__icontains=value) |
            Q(user__username__icontains=value) |
            Q(content__icontains=value) |
            Q(ticket_id__icontains=value)
        )

    
class VMWorkLogFilterSet(BaseFilterSet):
    """
    Virtual Machine Work Log Filter Set
    """
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    time = django_filters.DateTimeFromToRangeFilter()
    user = django_filters.ModelMultipleChoiceFilter(
        field_name='user__id',
        queryset=User.objects.all(),
        to_field_name='id',
        label='Author',
    )
    category = django_filters.ModelMultipleChoiceFilter(
        field_name='category__id',
        queryset=Category.objects.all(),
        to_field_name='id',
        label='Category',
    )

    class Meta:
        model = VMWorkLog
        fields = [
            'id', 'category', 'subject', 'user', 'content', 'internal_only', 'log_id', 'ticket_id', 'time'
        ]

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        return queryset.filter(
            Q(category__category__icontains=value) |
            Q(user__username__icontains=value) |
            Q(content__icontains=value) |
            Q(ticket_id__icontains=value)
        )
