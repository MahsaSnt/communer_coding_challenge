from rest_framework import routers
from django.urls import path

from .views import ProjectView, TaskView

router = routers.DefaultRouter()
router.register(r'project', ProjectView)

urlpatterns = router.urls + [
    path('project/<project_id>/task/', TaskView.as_view({'get': 'list', 'post': 'create'})),
    path('project/<project_id>/task/<pk>/', TaskView.as_view({'get': 'retrieve', 'patch': 'partial_update'}))
]
