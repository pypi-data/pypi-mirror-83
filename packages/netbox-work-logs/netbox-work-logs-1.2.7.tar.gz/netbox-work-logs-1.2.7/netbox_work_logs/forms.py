from django import forms
from django.contrib.auth.models import User

from utilities.forms import (
    BootstrapMixin, DateTimePicker, DynamicModelChoiceField, CommentField, DynamicModelMultipleChoiceField,
    SmallTextarea, StaticSelect2, APISelectMultiple,
    BOOLEAN_WITH_BLANK_CHOICES
)
from .models import Category, VMWorkLog, DeviceWorkLog

# 
# Device Work Log Filter Form and Edit Form
# 

class DeviceWorkLogFilterForm(BootstrapMixin, forms.Form):
    """
    Device Work Log Filter Form
    """
    model = DeviceWorkLog
    q = forms.CharField(
        required=False,
        label='Search'
    )
    time_after = forms.DateTimeField(
        label='After',
        required=False,
        widget=DateTimePicker()
    )
    time_before = forms.DateTimeField(
        label='Before',
        required=False,
        widget=DateTimePicker()
    )
    category = DynamicModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        display_field='category',
        label='Category',
        widget=APISelectMultiple(
            api_url='/api/plugins/work-logs/categories/',
        )
    )
    user = DynamicModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        display_field='username',
        label='Author',
        widget=APISelectMultiple(
            api_url='/api/users/users/',
        )
    )

class DeviceWorkLogEditForm(BootstrapMixin, forms.ModelForm):
    """
    Device Work Log Edit Form
    """
    category = forms.ModelChoiceField(
        queryset=Category.objects.all()
    )
    content = CommentField(
        widget=SmallTextarea,
        label='Content',
        required=False
    )
    internal_only = forms.NullBooleanField(
        widget=StaticSelect2(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        ),
        label='Internal Only',
        required=False
    )

    class Meta:
        model = DeviceWorkLog
        fields = [
            'subject', 'category', 'internal_only', 'content', 'ticket_id'
        ]
    
# 
# Virtual Machine Work Log Filter Form and Edit Form
#   

class VMWorkLogFilterForm(BootstrapMixin, forms.Form):
    """
    Virtual Machine Work Log Filter Form
    """
    model = VMWorkLog
    q = forms.CharField(
        required=False,
        label='Search'
    )
    time_after = forms.DateTimeField(
        label='After',
        required=False,
        widget=DateTimePicker()
    )
    time_before = forms.DateTimeField(
        label='Before',
        required=False,
        widget=DateTimePicker()
    )
    category = DynamicModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        display_field='category',
        label='Category',
        widget=APISelectMultiple(
            api_url='/api/plugins/work-logs/categories/',
        )
    )
    # action = forms.ChoiceField(
    #     choices=add_blank_choice(ObjectChangeActionChoices),
    #     required=False,
    #     widget=StaticSelect2()
    # )
    user = DynamicModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        display_field='username',
        label='Author',
        widget=APISelectMultiple(
            api_url='/api/users/users/',
        )
    )


class VMWorkLogEditForm(BootstrapMixin, forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all()
    )
    content = CommentField(
        widget = SmallTextarea,
        label='Content',
        required=False
    )
    internal_only = forms.NullBooleanField(
        widget=StaticSelect2(
            choices=BOOLEAN_WITH_BLANK_CHOICES
        ),
        label='Internal Only',
        required=False
    )
    class Meta:
        model = VMWorkLog
        fields = [
            'subject', 'category', 'internal_only', 'content', 'ticket_id'
        ]
    
