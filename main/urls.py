from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register('staff', StaffViewset),
router.register('auth', AuthViewset)
router.register('markaz', MarkazViewset)
router.register('course', CourseViewset)
router.register('room', RoomViewset)
router.register('history', HistoryViewset)
router.register('schedule', ClassScheduleViewset)
router.register('bots', BotViewset)
router.register('chat', ChatViewset)
router.register('messages', MessageViewset)
router.register('reply-message', SendReplyMessage)
router.register('course_plan', CoursePlanViewset)
router.register('course_extra', CourseGraduateViewset)
router.register('course_category', CourseDetailCategoryViewset)
router.register('teacher', TeacherViewset)
router.register('price', PriceViewset)