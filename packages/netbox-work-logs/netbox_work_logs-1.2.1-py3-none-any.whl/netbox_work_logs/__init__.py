from extras.plugins import PluginConfig

class WorkLogsConfig(PluginConfig):
    """
    This class defines attributes for the NetBox Work Logs plugin.
    """
    # Plugin package name
    name = 'netbox_work_logs'

    # Human-friendly name and description
    verbose_name = 'Work Logs'
    description = 'A plugin to render and edit work logs for each virtual machine and each device'

    # Plugin version
    version = '1.2'

    # Plugin author
    author = 'Vasilatos Vitaliy'
    author_email = 'vasilatos80@gmail.com'

    # Configuration parameters that MUST be defined by the user (if any)
    required_settings = []

    # Default configuration parameter values, if not set by the user
    # default_settings = {
    #     'loud': True
    # }

    # Base URL path. If not set, the plugin name will be used.
    base_url = 'work-logs'

    # Caching config
    # caching_config = {}


config = WorkLogsConfig
