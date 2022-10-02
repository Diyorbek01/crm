
from django.urls import path, include
from rest_framework import routers
from payment.views import *
from rest_framework.routers import DefaultRouter

payment_router = DefaultRouter()

payment_router.register('payment', PaymentViewSet)
payment_router.register('expense', ExpenseViewSet)
payment_router.register('category', CategoryViewSet)
payment_router.register('salary', SalaryViewSet)