from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import *
lead_router = DefaultRouter()

lead_router.register('form', LeadFormViewset),
lead_router.register('place', PlaceViewset),