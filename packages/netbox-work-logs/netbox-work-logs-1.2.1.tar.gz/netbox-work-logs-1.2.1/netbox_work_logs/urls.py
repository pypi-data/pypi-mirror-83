from django.urls import path
from . import views

urlpatterns = [
    path('vm-worklogs/<int:vm>/list/',
         views.VMWorkLogListView.as_view(), name='vmworklog_list'),
    path('vm-worklogs/<int:pk>/detail/',
         views.VMWorkLogDetailView.as_view(), name='vmworklog_detail'),
    path('vm-worklogs/<int:pk>/edit/',
         views.VMWorkLogEditView.as_view(), name='vmworklog_edit'),
    path('vm-worklogs/<int:pk>/delete/',
         views.VMWorkLogDeleteView.as_view(), name='vmworklog_delete'),
    path('device-worklogs/<int:device>/list/', 
         views.DeviceWorkLogListView.as_view(), name='deviceworklog_list'),
    path('device-worklogs/<int:pk>/detail/',
         views.DeviceWorkLogDetailView.as_view(), name='deviceworklog_detail'),
    path('device-worklogs/<int:pk>/edit/',
         views.DeviceWorkLogEditView.as_view(), name='deviceworklog_edit'),
    path('device-worklogs/<int:pk>/delete/',
         views.DeviceWorkLogDeleteView.as_view(), name='deviceworklog_delete'),
    
]
