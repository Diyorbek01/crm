from django.contrib import admin

# Register your models here.
from .models import Group, Week

# admin.site.register(Group)
admin.site.register(Week)

@admin.register(Group)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'teacher','days','room','start_lesson_at','start_lesson_at','start_group_at','finish_group_at', 'course', 'markaz')
    list_display_links = ('id', 'name', 'teacher','days','room','start_lesson_at','start_lesson_at','start_group_at','finish_group_at', 'course', 'markaz')
