from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import *

student_router = DefaultRouter()

student_router.register('student', StudentsViewSet),
student_router.register('attendance', AttendanceViewSet),
student_router.register('addgroup', AddGroupViewSet),
student_router.register('filteredstudent', StudentsAttandanceViewSet),

urlpatterns = [
    path('edit/<str:pk>', views.edit, name='edit' )
]