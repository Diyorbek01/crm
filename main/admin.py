from django.contrib import admin
from .models import *



@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_filter = ('markaz', 'role', 'is_active')
    list_display = ('id', 'phone', 'full_name', 'role', 'is_active')
    list_display_links = ('id', 'phone')\


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_filter = ( 'period', 'amount','discount')
    list_display = ('id', 'period', 'amount','discount')
    list_display_links = ('id', 'period')

  

@admin.register(Markaz)
class MarkazAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'registered_date')
    list_display_links = ('id', 'name', 'registered_date')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'markaz', 'name', 'price')
    list_display_links = ('id', 'markaz', 'name', 'price')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'markaz')
    list_display_links = ('id', 'name', 'markaz')


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'markaz', 'user', 'did', 'date')
    list_display_links = ('id', 'markaz', 'user', 'did', 'date')


admin.site.register(CoursePlan)
admin.site.register(CourseCategory)
admin.site.register(CourseGraduate)


admin.site.register(Bot)
admin.site.register(Chat)
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'chat', 'own')
    list_display_links = ('id', 'text', 'chat')