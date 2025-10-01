from rest_framework.routers import DefaultRouter
from .views import ProbeViewSet

router = DefaultRouter()
router.register(r'probes', ProbeViewSet, basename='probe')

urlpatterns = router.urls