from rest_framework.serializers import ModelSerializer
from netbox_work_logs.models import Category, VMWorkLog, DeviceWorkLog


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'category')

class VMWorkLogSerializer(ModelSerializer):
    
    class Meta:
        model = VMWorkLog
        fields = ('id', 'vm', 'user', 'category', 'subject', 'content', 'internal_only', 'ticket_id', 'time')
        
    def create(self, validated_data):
        return VMWorkLog.objects.create(**validated_data)

class DeviceWorkLogSerializer(ModelSerializer):
    
    class Meta:
        model = DeviceWorkLog
        fields = ('id', 'device', 'user', 'category', 'subject', 'content', 'internal_only', 'ticket_id', 'time')
