import uuid
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from utilities.querysets import RestrictedQuerySet


class Category(models.Model):
    """
    Work log category model
    """
    LABEL_CHOICES = (
        ('success', 'Green'),
        ('primary', 'Blue'),
        ('info', 'Cyan'),
        ('warning', 'Orange'),
        ('danger', 'Red')
    )
    category=models.CharField(max_length=50)
    category_label = models.CharField(max_length=10, choices=LABEL_CHOICES)
    
    class Meta:
        managed = True
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.category


class DeviceWorkLog(models.Model):
    """
    The Device work log entry is tracked in the Device work logs table.
    """
    time = models.DateTimeField(
        auto_now=True,
        editable=True,
        db_index=True
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name='devicelogs',
        blank=True,
        null=True
    )
    log_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    subject = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    content = models.TextField(
        blank=True,
        null=True
    )
    internal_only = models.BooleanField(
        default=False
    )
    ticket_id = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    device = models.ForeignKey(
        to="dcim.Device", 
        on_delete=models.CASCADE
    )
    
    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ["-time"]
    
    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse("plugins:netbox_work_logs:deviceworklog_detail", kwargs={"pk": self.pk})
    
class VMWorkLog(models.Model):
    """
    The VM work log entry is tracked in the VM work logs table.
    """
    time = models.DateTimeField(
        auto_now=True,
        editable=False, 
        db_index=True
    )
    user = models.ForeignKey(
        to=User, 
        on_delete=models.SET_NULL,
        related_name='vmlogs',
        blank=True,
        null=True
    )
    log_id = models.UUIDField(
        default=uuid.uuid4, 
        editable=False
    )
    category = models.ForeignKey(
        to=Category, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True
    )
    subject = models.CharField(
        max_length=200, 
        blank=True, 
        null=True
    )
    content = models.TextField(
        blank=True, 
        null=True
    )
    internal_only = models.BooleanField(
        default=False
    )
    ticket_id = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    vm = models.ForeignKey(
        to="virtualization.VirtualMachine", 
        on_delete=models.CASCADE
    )
    
    objects = RestrictedQuerySet.as_manager()

    class Meta:
        ordering = ["-time"]
        
    def __str__(self):
        return self.subject
        
    def get_absolute_url(self):
        return reverse("plugins:netbox_work_logs:vmworklog_detail", kwargs={"pk": self.pk})
    


    
