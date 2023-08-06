from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import APIRootView
from rest_framework.response import Response
from netbox_work_logs.models import Category, VMWorkLog, DeviceWorkLog
from .serializers import CategorySerializer, VMWorkLogSerializer, DeviceWorkLogSerializer

class WorkLogsRootView(APIRootView):
    """
    WorkLogs API root view
    """
    def get_view_name(self):
        return 'Work Logs'

# 
# Categories
# 

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# 
# VM Work Logs
# 

class VMWorkLogViewSet(ModelViewSet):
    queryset = VMWorkLog.objects.all()
    serializer_class = VMWorkLogSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.POST
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

# 
# Device Work Logs
# 

class DeviceWorkLogViewSet(ModelViewSet):
    queryset = DeviceWorkLog.objects.all()
    serializer_class = DeviceWorkLogSerializer
    
    def create(self, request, *args, **kwargs):
        data = request.POST
        serializer = self.get_serializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
