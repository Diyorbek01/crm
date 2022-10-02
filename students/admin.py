from django.contrib import admin
from .models import *


# admin.site.register(Attendance)
@admin.register(Students)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'markaz', 'name', 'phone', 'birthday', 'type', 'gender', 'comment', 'lead_category')
    list_display_links = ('id', 'markaz', 'name', 'phone', 'birthday', 'type', 'gender', 'comment', 'lead_category')


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'action', 'student', 'group', 'date')
    list_display_links = ('id', 'action', 'student', 'group', 'date')
