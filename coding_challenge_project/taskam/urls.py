from rest_framework import routers

from .views import ProjectView, TaskView

router = routers.DefaultRouter()
router.register(r'project', ProjectView)
router.register(r'task', TaskView)

urlpatterns = router.urls
