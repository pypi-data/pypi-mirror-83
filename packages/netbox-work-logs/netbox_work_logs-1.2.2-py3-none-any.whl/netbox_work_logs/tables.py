import django_tables2 as tables

from utilities.tables import (
    BaseTable, BooleanColumn, ButtonsColumn, ColorColumn, ColoredLabelColumn, TagColumn, ToggleColumn,
)
from .models import VMWorkLog, DeviceWorkLog

WORKLOG_TIME = """
<a href="{{ record.get_absolute_url }}">{{ value|date:"SHORT_DATETIME_FORMAT" }}</a>
"""
WORKLOG_SUBJECT = """
{% if record.get_absolute_url %}
    <a href="{{ record.get_absolute_url }}">{{ record.subject }}</a>
{% else %}
    {{ record.subject }}
{% endif %}
"""
WORKLOG_CATEGORY = """
<span class="label label-{{ record.category.category_label }}">{{ record.category.category }}</span>
"""
WORKLOG_INTERNAL_ONLY = """
{% if record.internal_only %}
<span class="label label-success"><i class="fa fa-check"></i></span>
{% endif %}
"""
class WorkLogsButtonsColumn(tables.TemplateColumn):
    """
    Render edit and delete buttons for a Device or a VM work log
    """
    buttons = ('edit', 'delete')
    attrs = {'td': {'class': 'text-right text-nowrap noprint'}}
    
    # Note that braces are escaped to allow for string formatting prior to template rendering
    template_code = """
    {{% if "edit" in buttons and perms.{app_label}.change_{model_name} %}}
        <a href="{{% url 'plugins:{app_label}:{model_name}_edit' {pk_field}=record.{pk_field} %}}?return_url={{{{ request.path }}}}" class="btn btn-xs btn-warning" title="Edit">
            <i class="fa fa-pencil"></i>
        </a>
    {{% endif %}}
    {{% if "delete" in buttons and perms.{app_label}.delete_{model_name} %}}
        <a href="{{% url 'plugins:{app_label}:{model_name}_delete' {pk_field}=record.{pk_field} %}}?return_url={{{{ request.path }}}}" class="btn btn-xs btn-danger" title="Delete">
            <i class="fa fa-trash"></i>
        </a>
    {{% endif %}}
    """
    
    def __init__(self, model, *args, pk_field='pk', buttons=None, prepend_template=None, **kwargs):
        if prepend_template:
            prepend_template = prepend_template.replace('{', '{{')
            prepend_template = prepend_template.replace('}', '}}')
            self.template_code = prepend_template + self.template_code

        template_code = self.template_code.format(
            app_label=model._meta.app_label,
            model_name=model._meta.model_name,
            pk_field=pk_field,
            buttons=buttons
        )

        super().__init__(template_code=template_code, *args, **kwargs)

        self.extra_context.update({
            'buttons': buttons or self.buttons,
        })

    def header(self):
        return ''
    

class DeviceWorkLogTable(BaseTable):
    """
    Device Work Log Table
    """
    time = tables.TemplateColumn(
        template_code=WORKLOG_TIME,
        verbose_name='Time'
    )
    subject = tables.TemplateColumn(
        template_code=WORKLOG_SUBJECT,
        verbose_name='Subject'
    )
    category = tables.TemplateColumn(
        template_code=WORKLOG_CATEGORY,
        verbose_name='Category'
    )
    user = tables.Column(
        verbose_name='Author'
    )
    ticket_id = tables.Column(
        verbose_name='Ticket ID'
    )
    internal_only = tables.TemplateColumn(
        template_code=WORKLOG_INTERNAL_ONLY,
        verbose_name='Internal Only'
    )
   

    actions = WorkLogsButtonsColumn(DeviceWorkLog, pk_field='pk')

    class Meta(BaseTable.Meta):
        model = VMWorkLog
        fields = ('pk', 'time', 'subject', 'category',
                  'user', 'ticket_id', 'internal_only', 'actions')
        default_columns = ('time', 'subject', 'category',
                           'user', 'ticket_id', 'internal_only', 'actions')


class VMWorkLogTable(BaseTable):
    """
    Virtual Machine Work Log Table
    """
    time = tables.TemplateColumn(
        template_code=WORKLOG_TIME,
        verbose_name='Time'
    )
    subject = tables.TemplateColumn(
        template_code=WORKLOG_SUBJECT,
        verbose_name='Subject'
    )
    category = tables.TemplateColumn(
        template_code=WORKLOG_CATEGORY,
        verbose_name='Category'
    )
    user = tables.Column(
        verbose_name='Author'
    )
    ticket_id = tables.Column(
        verbose_name='Ticket ID'
    )
    internal_only = tables.TemplateColumn(
        template_code=WORKLOG_INTERNAL_ONLY,
        verbose_name='Internal Only'
    )


    actions = WorkLogsButtonsColumn(VMWorkLog, pk_field='pk')

    class Meta(BaseTable.Meta):
        model = VMWorkLog
        fields = ('pk', 'time', 'subject', 'category', 'user', 'ticket_id', 'internal_only', 'actions')
        default_columns = ('time', 'subject', 'category',
                           'user', 'ticket_id', 'internal_only', 'actions')
        
