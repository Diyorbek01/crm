from rest_framework.routers import DefaultRouter

from . import views

group_router = DefaultRouter()

group_router.register('group', views.GroupViewset),

