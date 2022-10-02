from django.contrib import admin
from .models import *

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'where', 'full_name', 'course', 'markaz')
    list_display_links = ('id', 'where', 'full_name', 'course', 'markaz')


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
