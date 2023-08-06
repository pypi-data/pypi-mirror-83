import django_filters
from django.contrib.auth.models import User
from django.db.models import Q

from utilities.filters import BaseFilterSet
from dcim.models import Device
from virtualization.models import VirtualMachine
from .models import Category, VMWorkLog, DeviceWorkLog
from .choices import *

  
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
    device = django_filters.ModelMultipleChoiceFilter(
        field_name='device__id',
        queryset=Device.objects.all(),
        to_field_name='id',
        label='Device',
    )
    internal_only=django_filters.MultipleChoiceFilter(
        choices=InternalOnlyChoices,
        null_value=None
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
    vm = django_filters.ModelMultipleChoiceFilter(
        field_name='vm__id',
        queryset=VirtualMachine.objects.all(),
        to_field_name='id',
        label='VM'
    )
    internal_only = django_filters.MultipleChoiceFilter(
        choices=InternalOnlyChoices,
        null_value=None
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
