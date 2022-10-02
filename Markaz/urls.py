"""Markaz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from group.urls import group_router
from main.urls import router
from lead.urls import lead_router
from payment.urls import payment_router
from django.conf.urls.static import static
from django.conf import settings

from main.views import SendMessageByBot, chats, get_company, get_token, get_user_tg_ids, room
from students import views as st_views
from group import views as gr_views
from main import views as ma_views
from payment import views as pa_views
from students.urls import student_router
from lead import views as lead_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include(router.urls)),
    path('lead/', include(lead_router.urls)),
    path('group/', include(group_router.urls)),
    # path('group/', include("group.urls")),
    path('students/', include(student_router.urls)),
    path('finance/', include(payment_router.urls)),
    path('get_markaz', get_company),
    path('user-tg-ids', get_user_tg_ids),
    path('send-message-by-bot', SendMessageByBot.as_view()),
    path('get_token/', get_token),
    path('chats/', chats),
    path('room/<int:chat_id>/', room),

    # Edit
    path('student-edit/', st_views.edit, name='student-edit'),
    path('group-edit/<str:pk>', gr_views.edit, name='group-edit'),
    path('course-edit/', ma_views.Course_edit, name='course-edit'),
    path('payment-edit/<str:pk>', pa_views.edit, name='payment-edit'),
    path('room-edit/<str:pk>', ma_views.Room_edit, name='room-edit'),
    path('staff-edit/', ma_views.Staff_edit, name='staff-edit'),
    path('staffs-edit/<str:pk>', ma_views.staff_edit, name='staffs-edit'),
    path('lead-edit/<str:pk>', lead_views.edit, name='lead-edit'),
    path('markaz-edit/', ma_views.markaz_edit, name='markaz-edit'),

    path('api/payme/', include('paymeuz.urls'))

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
