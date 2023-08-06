from rest_framework import routers

from .views import CategoryViewSet, VMWorkLogViewSet, DeviceWorkLogViewSet, WorkLogsRootView


router = routers.DefaultRouter()
router.APIRootView = WorkLogsRootView

router.register('categories', CategoryViewSet)
router.register('vm-logs', VMWorkLogViewSet)
router.register('device-logs', DeviceWorkLogViewSet)

app_name = 'netbox_work_logs-api'
urlpatterns = router.urls
