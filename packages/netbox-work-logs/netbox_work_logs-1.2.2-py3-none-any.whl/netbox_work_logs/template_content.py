from django.contrib.auth.context_processors import PermWrapper

from extras.plugins import PluginTemplateExtension
from .models import VMWorkLog, DeviceWorkLog, Category


class DeviceWorkLogs(PluginTemplateExtension):
    """
    Display work logs block on individual device page.
    """
    model = 'dcim.device'
    
    def buttons(self):
        context = {
            'perms': PermWrapper(self.context['request'].user),
        }
        return self.render('netbox_work_logs/device/inc/logslist_btn.html', context)
    
    def right_page(self):
        
        # get latest 5 logs
        logs = DeviceWorkLog.objects.filter(
            device=self.context['object'].id).order_by('-time')[:5]
        
        return self.render('netbox_work_logs/device/latest_logs.html', extra_context={
            'work_logs': logs,
        })
        
    
class VMWorkLogs(PluginTemplateExtension):
    """
    Display work logs block on individual virtual machine page.
    """
    model = 'virtualization.virtualmachine'
    
    def buttons(self):
        
        context = {
            'perms': PermWrapper(self.context['request'].user),
        }
       
        return self.render('netbox_work_logs/vm/inc/logslist_btn.html', context)
    
    def right_page(self):
        
        # get latest 5 logs
        logs = VMWorkLog.objects.filter(
            vm=self.context['object'].id).order_by('-time')[:5]
        
        return self.render('netbox_work_logs/vm/latest_logs.html', extra_context={
            'work_logs': logs,
        })

# PluginTemplateExtension subclasses must be package into an iterable named
# template_extensions to be imported by NetBox.
template_extensions = [DeviceWorkLogs, VMWorkLogs]
