from dateutil.relativedelta import relativedelta
from datetime import date
from datetime import timedelta
from group.models import Week
from payment.models import Payment
from students.serializers import *
from students.models import *
from datetime import datetime, timedelta


class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Week
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    number_student = serializers.SerializerMethodField('get_student')
    name_teacher = serializers.SerializerMethodField('get_teacher')
    name_room = serializers.SerializerMethodField('get_room')
    name_course = serializers.SerializerMethodField('get_course')
    number_month = serializers.SerializerMethodField('count_month')
    name_month = serializers.SerializerMethodField('get_month')
    name_week = serializers.SerializerMethodField('get_week')
    group_price = serializers.SerializerMethodField('get_price')

    def get_student(self, result):
        group_id = getattr(result, "id")
        result = Students.objects.filter(group=group_id).count()
        return result

    def get_teacher(self, result):
        teacher_id = getattr(result, "teacher_id")
        result = Group.objects.filter(teacher_id=teacher_id)
        for i in result:
            name = i.teacher.full_name
            return name

    def get_room(self, result):
        room_id = getattr(result, "room")
        result = Group.objects.filter(room_id=room_id)
        for i in result:
            name = i.room.name
            return name

    def get_course(self, result):
        course_id = getattr(result, "course_id")

        result = Group.objects.filter(course_id=course_id)
        for i in result:
            name = i.course.name
            return name

    def get_month(self, result):
        start = getattr(result, "start_group_at")
        finish = getattr(result, "finish_group_at")
        startm = int(start.month)
        starty = int(start.year)
        finishy = int(finish.year)
        delta = finish - start
        r = relativedelta(finish, start)
        result = int(r.months + (12 * r.years))
        mon = []
        years = []
        for i in range(starty, finishy):
            years.append(i)
        for i in range(startm, startm + result + 1):
            mo = i % 12
            mon.append(mo)
        return mon

    def get_week(self, result):
        start = getattr(result, "start_group_at")
        finish = getattr(result, "finish_group_at")
        startm = int(start.month)
        starty = int(start.year)
        finishy = int(finish.year)
        delta = finish - start
        r = relativedelta(finish, start)
        result = int(r.months + (12 * r.years))
        mon = []
        years = []
        weekd = []
        for i in range(starty, finishy):
            years.append(i)
        for i in range(startm, startm + result + 1):
            mo = i % 12
            mon.append(mo)
        for i in range(delta.days):
            futuredays = start + timedelta(days=i + 1)
            week = futuredays.weekday()
            result = {
                "yil": futuredays.year,
                "oy": futuredays.month,
                "kun": futuredays.day,
                "hafta": week,

            }
            weekd.append(result)
        return weekd

    def count_month(self, result):
        start = getattr(result, "start_group_at")
        finish = getattr(result, "finish_group_at")
        delta = finish - start
        number = 0
        for i in range(delta.days):
            number += 1
        result = number / 30

        return round(result)

    def get_price(self, result):
        course_id = getattr(result, "course_id")
        group_id = getattr(result, "id")
        students = Students.objects.filter(group=group_id).count()
        result = Group.objects.raw('''SELECT gr.id, gr.name as name, course.name as course_name, course.price as price, gr.student as plan_student,count(student.id) as total_student,
count(students.id) as paid_student, count(student.id)*100/gr.student as percent_student from group_group as gr

LEFT JOIN main_course as course on course.id = gr.course_id
LEFT JOIN students_students_group as student on student.group_id = gr.id
LEFT JOIN payment_payment as students on students.id= student.id
where gr.id=%s and gr.typ="Yangi"
GROUP by gr.id''', [group_id])
        data = []
        for i in result:
            data.append({
                "id": i.id,
                "gr_name": i.name,
                "course_name": i.course_name,
                "price": i.price,
                "total_student": i.total_student,
                "plan_student": i.plan_student,
                "paid_student": i.paid_student,
                "percent_student": i.percent_student,
            })
        return data

    class Meta:
        model = Group
        fields = ['id', 'name', 'course', 'teacher', 'days', 'room', 'student',
                  'start_group_at', 'start_lesson_at', 'finish_group_at',
                  'typ', 'create_at', 'update_at', 'week', 'markaz', 'name_teacher', 'name_course', 'name_room',
                  'number_student', 'name_month', 'name_week', 'group_price', 'number_month']


class GroupGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
