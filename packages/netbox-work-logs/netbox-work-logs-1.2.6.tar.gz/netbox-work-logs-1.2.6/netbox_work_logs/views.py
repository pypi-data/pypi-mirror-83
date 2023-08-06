import logging
import time
from django.views.generic import View
from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django_tables2 import RequestConfig

from utilities.views import (
    GetReturnURLMixin, ObjectView, ObjectEditView, ObjectDeleteView, ObjectListView,
)
from utilities.paginator import EnhancedPaginator, get_paginate_count
from virtualization.models import VirtualMachine
from dcim.models import Device
from .models import VMWorkLog, DeviceWorkLog
from . import tables, filters, forms

# 
# Device Work Log
# 
class DeviceWorkLogListView(View):
    """
    Present a history of changes made to a particular virtual machine.
    """
    queryset = None
    filterset = filters.DeviceWorkLogFilterSet
    filterset_form = forms.DeviceWorkLogFilterForm
    table = tables.DeviceWorkLogTable
    template_name = 'netbox_work_logs/device/worklog/worklog_list.html'
    
    def get(self, request, device, **kwargs):
        logger = logging.getLogger('netbox_work_logs.views.DeviceWorkLogListView')
        # Handle QuerySet restriction of parent object if needed
        if hasattr(Device.objects, 'restrict'):
            obj = get_object_or_404(Device.objects.restrict(
                request.user, 'view'), id=device)
        else:
            obj = get_object_or_404(Device, id=device)
        
        self.queryset = DeviceWorkLog.objects.restrict(request.user, 'view').prefetch_related(
                'user', 'device'
            ).filter(
                Q(device=device)
            )
        if self.filterset:
            self.queryset = self.filterset(request.GET, self.queryset).qs

        table = tables.DeviceWorkLogTable(
            self.queryset,
            orderable=True
        )
        
        # Apply the request context
        paginate = {
            'paginator_class': EnhancedPaginator,
            'per_page': get_paginate_count(request)
        }
        RequestConfig(request, paginate).configure(table)

        context = {
            'table': table,
            'obj': obj,
            'filter_form': self.filterset_form(request.GET, label_suffix='') if self.filterset_form else None,
        }

        return render(request, self.template_name, context)
    
    def alter_queryset(self, request):
        # .all() is necessary to avoid caching queries
        return self.queryset.all()


class DeviceWorkLogDetailView(ObjectView):
    """
    Detail Device Work Log View
    """
    queryset = DeviceWorkLog.objects.prefetch_related('user', 'device')

    def get(self, request, pk):
        deviceworklog = get_object_or_404(self.queryset, pk=pk)
        return render(request, 'netbox_work_logs/device/worklog/worklog_detail.html', {'deviceworklog': deviceworklog})


class DeviceWorkLogEditView(ObjectEditView):
    queryset = DeviceWorkLog.objects.all()
    model_form = forms.DeviceWorkLogEditForm
    template_name = 'netbox_work_logs/device/worklog/worklog_edit.html'


class DeviceWorkLogDeleteView(ObjectDeleteView):
    queryset = DeviceWorkLog.objects.all()

# 
# VM Work Log
# 

class VMWorkLogListView(View):
    """
    Present a history of changes made to a particular virtual machine.
    """
    queryset = None
    filterset = filters.VMWorkLogFilterSet
    filterset_form = forms.VMWorkLogFilterForm
    table = tables.VMWorkLogTable
    template_name = 'netbox_work_logs/vm/worklog/worklog_list.html'
    
    def get(self, request, vm, **kwargs):
        logger = logging.getLogger('netbox_work_logs.views.VMWorkLogListView')
        # Handle QuerySet restriction of parent object if needed
        if hasattr(VirtualMachine.objects, 'restrict'):
            obj = get_object_or_404(VirtualMachine.objects.restrict(
                request.user, 'view'), id=vm)
        else:
            obj = get_object_or_404(VirtualMachine, id=vm)
            
        self.queryset = VMWorkLog.objects.restrict(request.user, 'view').prefetch_related(
                'user', 'vm'
            ).filter(
                Q(vm=vm)
            )

        if self.filterset:
            self.queryset = self.filterset(request.GET, self.queryset).qs

        # # Construct the table based on the user`s permissions
        # if request.user.is_authenticated:
        #     columns = request.user.config.get(f"tables.")
        # else:
        #     columns = None
            
        table = tables.VMWorkLogTable(
            self.queryset,
            orderable=True
        )
        
        # Apply the request context
        paginate = {
            'paginator_class': EnhancedPaginator,
            'per_page': get_paginate_count(request)
        }
        RequestConfig(request, paginate).configure(table)

        context = {
            'table': table,
            'obj': obj,
            'filter_form': self.filterset_form(request.GET, label_suffix='') if self.filterset_form else None,
        }
        
        return render(request, self.template_name, context)
    
    def alter_queryset(self, request):
        # .all() is necessary to avoid caching queries
        return self.queryset.all()
    
class VMWorkLogDetailView(ObjectView):
    """
    Detail VM work log view
    """
    queryset = VMWorkLog.objects.prefetch_related('user', 'vm')
    
    def get(self, request, pk):
        vmworklog = get_object_or_404(self.queryset, pk=pk)
        return render(request, 'netbox_work_logs/vm/worklog/worklog_detail.html', {'vmworklog': vmworklog})
    
class VMWorkLogEditView(ObjectEditView):
    queryset = VMWorkLog.objects.all()
    model_form = forms.VMWorkLogEditForm
    template_name = 'netbox_work_logs/vm/worklog/worklog_edit.html'

class VMWorkLogDeleteView(ObjectDeleteView):
    queryset = VMWorkLog.objects.all()


    
