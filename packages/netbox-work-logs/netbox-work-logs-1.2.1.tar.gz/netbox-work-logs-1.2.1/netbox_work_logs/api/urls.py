from rest_framework import routers

from .views import CategoryViewSet, VMWorkLogViewSet, DeviceWorkLogViewSet


router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('vm-logs', VMWorkLogViewSet)
router.register('device-logs', DeviceWorkLogViewSet)

urlpatterns = router.urls
