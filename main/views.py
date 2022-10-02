from django.shortcuts import render
import os
from django.db.models import Q
from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action, renderer_classes, api_view
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

import requests
from django.conf import settings

from group.models import *
from group.serializers import GroupSerializer, WeekSerializer
from lead.models import Lead
from students.models import Students
from utilities import get_markaz
from .serializers import *


class AuthViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Staff.objects.all()
    serializer_class = AuthSerializer

    @action(methods=['post'], detail=False)
    def login(self, request):

        # try:
        password = request.data.get('password')
        phone = request.data.get('phone')

        markaz = get_markaz(request)

        if Staff.objects.filter(markaz_id=markaz.id, phone=phone, password=password).exists():
            staff = Staff.objects.filter(markaz_id=markaz.id, phone=phone, password=password)
            # history = History.objects.create(markaz_id=markaz_id, user=staff, did="Yangi hodim yaratdi")
            data = self.get_serializer_class()(staff, many=True)

            return Response(data.data, status=200)

        else:
            return Response({'result': 'bunday hodim mavjud emas'}, status=401)


class PriceViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Price.objects.all()
    serializer_class = PriceSerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        price = Price.objects.all()
        data = self.get_serializer_class()(price, many=True)

        return Response(data.data, status=200)

    @action(methods=['post'], detail=False)
    def post(self, request):
        post = request.data
        serializer = PriceSerializer(data=post)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class TeacherViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Staff.objects.filter(role="Teacher", typ='Appear')
    serializer_class = StaffSerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz']

        # staff = Staff.objects.filter(markaz_id=markaz_id, role="Teacher")

        # data = self.get_serializer_class()(staff, many=True)
        teacher = Staff.objects.filter(role="Teacher", typ='Appear', markaz_id=markaz_id)
        data = []

        for i in teacher:
            number_gr = Group.objects.filter(markaz_id=markaz_id, teacher_id=i.id).count()
            data.append({
                'birthdate': i.birthdate,
                'date_joined': i.date_joined,
                'full_name': i.full_name,
                'gender': i.gender,
                'id': i.id,
                'markaz': i.markaz.id,
                'role': i.role,
                'password': i.password,
                'phone': i.phone,
                'photo': '/media/' + i.photo.name,
                'number_gr': number_gr
            })
            # photo = i.photo
        return Response(data, status=200, content_type="image/png")

    @action(methods=['get'], detail=False)
    def get_photo(self, request):
        markaz_id = request.GET['markaz']
        teacher = request.GET['teacher']

        staff = Staff.objects.get(markaz_id=markaz_id, role="Teacher", id=teacher)

        return Response(staff.photo.file, status=200)

    @action(methods=['get'], detail=False)
    def statistic(self, request):
        markaz_id = request.GET['markaz']
        teacher = Staff.objects.filter(markaz=markaz_id, role='Teacher', typ='Appear').count()
        student = Students.objects.filter(markaz=markaz_id, type=1).count()
        course = Course.objects.filter(markaz=markaz_id, typ='Appear').count()
        group = Group.objects.filter(markaz=markaz_id, typ='Jarayonda').count()
        leads = Lead.objects.filter(Q(markaz=markaz_id) | Q(status='Yangi') | Q(status='Aloqada')).count()
        # debtor =
        data = [{
            'teacher': teacher,
            'student': student,
            'course': course,
            'group': group,
            'leads': leads,
        }]
        return Response(data, status=200)

    @action(methods=['get'], detail=False)
    def get_group(self, request):
        markaz_id = request.GET['markaz']
        teacher = request.GET['teacher_id']

        staff = Staff.objects.raw('''SELECT teacher.id,teacher.phone,teacher.full_name, teacher.birthdate, teacher.gender, teacher.photo, teacher.date_joined,
gr.id as gr_id, gr.name as gr_name, count(student.students_id) as number_student from main_staff as teacher
LEFT JOIN group_group as gr on teacher.id=gr.teacher_id
LEFT JOIN students_students_group as student on student.group_id=gr.id

where role='Teacher' and teacher.id=%s and teacher.markaz_id=%s
GROUP by gr.id''', [teacher, markaz_id])
        data = []
        for i in staff:
            data.append({
                "id": i.id,
                "birhtdate": i.birthdate,
                "gender": i.gender,
                "phone": i.phone,
                "date_joined": i.date_joined,
                "full_name": i.full_name,
                "number_student": i.number_student,
                "gr_name": i.gr_name,
                "gr_id": i.gr_id,
            })
        return Response(data)

    @action(methods=['post'], detail=False)
    def add(self, request):
        post = request.data
        print(post)
        phone = post['phone']
        full_name = post['full_name']
        birthdate = post['birthdate']
        gender = post['gender']
        password = post['password']
        markaz_id = post['markaz']
        staff = post['staff']
        image = request.data['photo']

        if Staff.objects.filter(phone=phone, markaz_id=markaz_id).exists():
            return Response({'result': "Telefon raqam boshqa hodimga tegishli"})

        else:
            if image == 'hello':
                teacher = Staff.objects.create(phone=phone, full_name=full_name, role="Teacher", birthdate=birthdate,
                                               gender=gender, password=password, markaz_id=markaz_id
                                               # , photo=photo
                                               )
            else:
                photo = request.FILES['photo']
                teacher = Staff.objects.create(phone=phone, full_name=full_name, role="Teacher", birthdate=birthdate,
                                               gender=gender, password=password, markaz_id=markaz_id
                                               , photo=photo
                                               )
            history = History.objects.create(markaz_id=markaz_id, user=staff, did="Yangi o'qituvchi yaratdi")

            serializer = self.get_serializer_class()(teacher)
            return Response(serializer.data)


@api_view(['post'])
def Staff_edit(request):
    staff = request.data['staff']
    markaz_id = request.data['markaz']
    id = request.data['id']
    phone = request.data['phone']
    full_name = request.data['full_name']
    birthdate = request.data['birthdate']
    gender = request.data['gender']
    # photo = request.FILES['photo']
    image = request.data['photo']
    password = request.data['password']
    student = Staff.objects.get(id=id)
    if image == "hello":
        # student.photo = photo,
        student.markaz_id = markaz_id
        student.phone = phone
        student.full_name = full_name
        student.birthdate = birthdate
        student.gender = gender
        student.password = password
        student.save()
    else:
        photo = request.FILES['photo']
        student.photo = photo
        student.markaz_id = markaz_id
        student.phone = phone
        student.full_name = full_name
        student.birthdate = birthdate
        student.gender = gender
        student.password = password
        student.save()
    data = {
        'photo': '/media/' + student.photo.name,
        'phone': student.phone,
        'full_name': student.full_name,
        'birthdate': student.birthdate,
        'password': student.password,
        'gender': student.gender,
        'id': student.id,
    }
    history = History.objects.create(markaz_id=markaz_id, user=staff, did="O'qituvchi ma'lumotlarini o'zgartirdi")

    return Response(data)


class StaffViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz']

        staff = Staff.objects.filter(~Q(role="Teacher"), markaz_id=markaz_id)
        data = []

        for i in staff:
            data.append({
                'id': i.id,
                'phone': i.phone,
                'full_name': i.full_name,
                'role': i.role,
                'birthdate': i.birthdate,
                'gender': i.gender,
                'photo': i.photo.name,
                'password': i.password,
                'typ': i.typ,
                # 'markaz':i.markaz,
                'date_joined': str(i.date_joined)[:10],
            })

        # data = self.get_serializer_class()(staff, many=True)

        return Response(data, status=200)

    @action(methods=['post'], detail=False)
    def add(self, request):
        post = request.data
        phone = post['phone']
        full_name = post['full_name']
        role = post['role']
        birthdate = post['birthdate']
        gender = post['gender']
        password = post['password']
        markaz_id = post['markaz']
        # photo = request.FILES['photo']

        if Staff.objects.filter(phone=phone, markaz_id=markaz_id).exists():
            return Response({'result': "Telefon raqam boshqa hodimga tegishli"})

        else:
            staff = Staff.objects.create(phone=phone, full_name=full_name, role=role, birthdate=birthdate,
                                         gender=gender, password=password, markaz_id=markaz_id
                                         # , photo=photo
                                         )
            history = History.objects.create(markaz_id=markaz_id, user=staff, did="Yangi hodim yaratdi")

            data = {
                'phone': staff.phone,
                'full_name': staff.full_name,
                'role': staff.role,
                'birthdate': staff.birthdate,
                'gender': staff.gender,
                'photo': staff.photo.name,
                'password': staff.password,
                'typ': staff.typ,
                # 'markaz':staff.markaz,
                'date_joined': str(staff.date_joined)[:10],
            }

            # serializer = self.get_serializer_class()(staff)
            return Response(data, status=201)

    @action(methods=['post'], detail=False)
    def delete(self, request):
        data = request.data
        markaz = data['markaz']
        staff = data['staff']
        staff_id = data['staff_id']
        history = History.objects.create(markaz_id=markaz, user=staff, did="Hodimni o'chirdi")

        staff = Staff.objects.get(id=staff_id)
        staff.typ = "Delete"
        staff.save()
        return Response({"id": staff.id}, status=200)


@api_view(['post'])
def staff_edit(request, pk):
    staff = request.data['staff']
    markaz_id = request.data['markaz']
    student = Staff.objects.get(id=pk)
    serializer = StaffSerializer(instance=student, data=request.data)
    if serializer.is_valid():
        serializer.save()
        history = History.objects.create(markaz_id=markaz_id, user=staff, did="Hodim ma'lumotlarini o'zgartirdi")

        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


class MarkazViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Markaz.objects.all()
    serializer_class = MarkazSerializer

    @action(methods=['post'], detail=False)
    def new(self, request):
        post = request.data
        name = post['name']
        phone = post['owner_phone']
        owner_full_name = post['owner_full_name']
        password = post['password']

        markaz = Markaz.objects.create(name=name)
        owner = Staff.objects.create(phone=phone, full_name=owner_full_name, role='Owner', password=password,
                                     markaz=markaz)

        result = f"""Yangi markaz qo'shildi.
                    Nomi: {markaz.name}  ,
                    Telefon: {owner.phone},
                    Egasi: {owner.full_name},
                    Ro'yxatga olingan sana: {markaz.registered_date}
                """
        return Response({'result': result})

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz']
        data = []
        markaz = Markaz.objects.get(id=markaz_id)
        owner = Staff.objects.get(role="Owner")
        data.append({
            "markaz_id": markaz.id,
            "markaz_name": markaz.name,
            "owner_name": owner.full_name,
            "owner_id": owner.id,
            "owner_password": owner.password,
            "owner_phone": owner.phone,
            # "markaz_id":markaz.id,
        })

        return Response(data)


    @action(methods=['get'], detail=False)
    def get_photo(self, request):
        markaz_id = request.GET['markaz']

        markaz = Markaz.objects.get(id=markaz_id)

        photo = {
            "photo": "/media/" + markaz.photo.name
        }
        return Response(photo, status=200)



@api_view(['post'])
def markaz_edit(request):
    staff = request.data['staff']
    markaz_id = request.data['markaz']
    name = request.data['name']
    phone = request.data['owner_phone']
    full_name = request.data['owner_full_name']
    password = request.data['password']
    image = request.data['photo']
    markazz = Markaz.objects.get(id=markaz_id)
    staffs = Staff.objects.get(role="Owner")

    if image == "hello":
        staffs.phone = phone
        staffs.full_name = full_name
        staffs.password = password
        markazz.name = name
        staffs.save()
        markazz.save()
    else:
        photo = request.FILES['photo']
        markazz.photo = photo
        staffs.phone = phone
        staffs.full_name = full_name
        staffs.password = password
        markazz.name = name
        staffs.save()
        markazz.save()

    data = {
        'photo': '/media/' + markazz.photo.name if markazz.photo else "/media/",
        "owner_phone": phone,
        "owner_name": full_name,
        "owner_password": password,
        "markaz_name": name,
        "owner_id": staffs.id
    }

    history = History.objects.create(markaz_id=markaz_id, user=staff, did="Markaz ma'lumotlarini o'zgartirdi")

    return Response(data)


# course
class CourseViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(methods=['post'], detail=False)
    def post(self, request):
        data = request.data
        print(data)
        markaz_id = data['markaz']
        name = data['name']
        price = data['price']
        description = data['description']
        duration = data['duration']
        staff = data['staff']
        image = data['photo']
        # photo = request.FILES['photo']
        #
        if image == 'hello':
            course = Course.objects.create(markaz_id=markaz_id, name=name, price=price, duration=duration,
                                           description=description)
        else:
            photo = request.FILES['photo']
            course = Course.objects.create(markaz_id=markaz_id, name=name, price=price, duration=duration, photo=photo,
                                           description=description)
        history = History.objects.create(markaz_id=markaz_id, user=staff, did="Yangi Kurs qo'shdi")
        serializer = self.get_serializer_class()(course)
        return Response(serializer.data, status=201)
        # return Response({"result": "Course created"}, status=201)

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz']

        courses = Group.objects.raw('''SELECT gr.name, gr.id,course.id as course_id, course.name as course_name, course.description, course.duration, 
course.price,course.photo, count(student.students_id) as number_student from group_group as gr
left join main_course as course on course.id = gr.course_id
left JOIN students_students_group as student on student.group_id=gr.id
where gr.markaz_id = %s
GROUP by course.id''', [markaz_id])
        data = []
        for i in courses:
            data.append({
                "name": i.course_name,
                "gr_id": i.id,
                "course_id": i.course_id,
                "gr_name": i.name,
                "price": i.price,
                'number_student': i.number_student,
                "duration": i.duration,
                "description": i.description,
                "photo": i.photo,
            })

        return Response(data)

    @action(methods=['post'], detail=False)
    def delete(self, request):
        data = request.data
        markaz = data['markaz']
        staff = data['staff']
        course_id = data['course_id']

        course = Course.objects.get(id=course_id)
        course.typ = "Delete"
        course.save()
        history = History.objects.create(markaz_id=markaz, user=staff, did="Kurs ma'lumotini o'chirdi")
        return Response("Deleted", status=200)


@api_view(['post'])
def Course_edit(request):
    staff = request.data['staff']
    markaz_id = request.data['markaz']
    id = request.data['id']
    name = request.data['name']
    price = request.data['price']
    duration = request.data['duration']
    description = request.data['description']
    # photo = request.FILES['photo']
    image = request.data['photo']
    student = Course.objects.get(id=id)
    if image == "hello":

        student.markaz_id = markaz_id
        student.name = name
        student.price = price
        student.duration = duration
        student.description = description
        student.save()
    else:
        photo = request.FILES['photo']
        student.photo = photo
        student.markaz_id = markaz_id
        student.name = name
        student.price = price
        student.duration = duration
        student.description = description
        student.save()
    data = {

        'photo': '/media/' + student.photo.name if student.photo else "/media/",
        'name': student.name,
        'price': student.price,
        'duration': student.duration,
        'description': student.description,
        'id': student.id,
    }
    history = History.objects.create(markaz_id=markaz_id, user=staff, did="Kurs ma'lumotlarini o'zgartirdi")

    return Response(data)


# course details
class CourseDetailCategoryViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz']
        # print(request.GET)
        course_id = request.GET['course_id']

        plan = CourseCategory.objects.filter(markaz_id=markaz_id, course_id=course_id)
        data = self.get_serializer_class()(plan, many=True)

        return Response(data.data, status=200)

    @action(methods=['post'], detail=False)
    def post(self, request):
        post = request.data
        title = post['name']
        staff = post['staff']
        markaz_id = post['markaz']
        course_id = post['course_id']

        plan = CourseCategory.objects.create(name=title, markaz_id=markaz_id, course_id=course_id, )
        history = History.objects.create(markaz_id=markaz_id, user=staff, did="Kurs ma'lumotlari uchun bo'lim qo'shdi")

        serializer = self.get_serializer_class()(plan)
        return Response(serializer.data, status=201)


# course details
class CoursePlanViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CoursePlan.objects.all()
    serializer_class = CoursePlanSerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz']
        course_id = request.GET['course_id']

        plan = CoursePlan.objects.filter(markaz_id=markaz_id, course_id=course_id)
        data = self.get_serializer_class()(plan, many=True)

        return Response(data.data, status=200)

    @action(methods=['post'], detail=False)
    def post(self, request):
        post = request.data
        title = post['title']
        category = post['category']
        duration = post['duration']
        staff = post['staff']
        markaz_id = post['markaz']
        course_id = post['course_id']

        plan = CoursePlan.objects.create(title=title, category_id=category, duration=duration, markaz_id=markaz_id,
                                         course_id=course_id, )
        history = History.objects.create(markaz_id=markaz_id, user=staff, did="Kurs uchun bo'lim qo'shdi")

        serializer = self.get_serializer_class()(plan)
        return Response(serializer.data)


# course details
class CourseGraduateViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = CourseGraduate.objects.all()
    serializer_class = CourseGraduateSerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz']
        course_id = request.GET['course_id']

        plan = CourseGraduate.objects.filter(markaz_id=markaz_id, course_id=course_id)
        data = self.get_serializer_class()(plan, many=True)

        return Response(data.data, status=200)

    @action(methods=['post'], detail=False)
    def post(self, request):
        post = request.data
        print(post)
        title = post['title']
        staff = post['staff']
        markaz_id = post['markaz']
        course_id = post['course_id']

        plan = CourseGraduate.objects.create(title=title, markaz_id=markaz_id, course_id=course_id)
        history = History.objects.create(markaz_id=markaz_id, user=staff, did="Kurs uchun foydali qo'llanma qo'shdi")

        serializer = self.get_serializer_class()(plan)
        return Response(serializer.data, status=201)


# room
class RoomViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz']
        room = Room.objects.filter(markaz_id=markaz_id, typ="Appear")

        data = self.get_serializer_class()(room, many=True)

        return Response(data.data)

    @action(methods=['post'], detail=False)
    def post(self, request):
        data = request.data
        markaz_id = data['markaz']
        name = data['name']
        staff = data['staff']

        room = Room.objects.create(markaz_id=markaz_id, name=name)
        history = History.objects.create(markaz_id=markaz_id, user=staff, did="Yangi xona qo'shdi")

        serializer = self.get_serializer_class()(room)

        return Response(serializer.data)

    @action(methods=['post'], detail=False)
    def delete(self, request):
        data = request.data
        markaz = data['markaz']
        staff = data['staff']
        room_id = data['room_id']
        history = History.objects.create(markaz_id=markaz, user=staff, did="Xona ma'lumotini o'chirdi")

        room = Room.objects.get(id=room_id)
        room.typ = "Delete"
        room.save()
        return Response({"id": room.id}, status=200)


@api_view(['post'])
def Room_edit(request, pk):
    staff = request.data['staff']
    markaz_id = request.data['markaz']
    student = Room.objects.get(id=pk)
    serializer = RoomSerializer(instance=student, data=request.data)
    if serializer.is_valid():
        serializer.save()
        history = History.objects.create(markaz_id=markaz_id, user=staff, did="Xona ma'lumotlarini o'zgartirdi")

        return Response(serializer.data, status=200)
    return Response(serializer.errors, status=400)


# history
class HistoryViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz']

        courses = History.objects.filter(markaz_id=markaz_id)

        data = self.get_serializer_class()(courses, many=True)

        return Response(data.data)


class ClassScheduleViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz = request.GET['markaz']
        week_days = Week.objects.all()
        groups = Group.objects.filter(markaz_id=markaz)
        data = []

        groups_list = []
        teachers_list = []
        rooms_list = []
        times_list = []
        for week_day in week_days:

            for group in groups:
                i = 0
                for day in group.week.all():
                    i = i + 1
                    if day.id == week_day.id:
                        day = {
                            'week_day': week_day.name,
                            'groups': group.name,
                            'teachers': group.teacher.full_name,
                            'rooms': group.room.name,
                            'times': str(group.start_lesson_at)[:-3]
                        }
                        data.append(day)

        return Response(data, status=200)


class BotViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Bot.objects.all()
    serializer_class = BotSerializer

    @action(methods=['post'], detail=False)
    def add(self, request):
        token = request.POST['token']
        markaz_id = request.POST['markaz_id']

        base_bot = str(settings.BASE_DIR) + '/bot.py'
        new_bot = str(settings.BASE_DIR) + '/bots/bot_{}.py'.format(markaz_id)
        bot_conf = str(settings.BASE_DIR) + "/conf/bot.conf"
        bot_conf_new = "/etc/supervisor/conf.d/bot_{}.conf".format(markaz_id)

        with open(base_bot) as f:
            new_code = f.read().replace('API_TOKEN = None', 'API_TOKEN = "' + token + '"')

        with open(new_bot, "w") as f:
            f.write(new_code)

        with open(bot_conf) as f:
            newText = f.read().replace('[program:bot]', '[program:bot_{}]'.format(markaz_id))
            new_conf = newText.replace('command=python3 /rootcrm/bot.py',
                                       'command=python3  /rootcrm/bots/bot_{}.py'.format(markaz_id))
            new_conf = new_conf.replace('stderr_logfile=/var/log/bot.err.log',
                                        'stderr_logfile=/var/log/bot_{}.err.log'.format(markaz_id))
            new_conf = new_conf.replace('stdout_logfile=/var/log/bot.out.log',
                                        'stderr_logfile=/var/log/bot_{}.out.log'.format(markaz_id))
            print(newText)

        with open(bot_conf_new, "w") as f:
            f.write(new_conf)

        bot = Bot.objects.create(markaz_id=markaz_id, token=token)

        # start bot
        os.system("supervisorctl reread")
        os.system("supervisorctl update")
        os.system("supervisorctl restart bot_{}".format(markaz_id))

        data = {
            'markaz_id': bot.markaz.id,
            'token': bot.token,
        }

        return Response(data, status=201)


class SendMessageByBot(APIView):
    def post(self, request):
        chat_id = request.POST['chat_id']
        token = request.POST['token']
        first_name = request.POST['first_name']
        text = request.POST['text']

        bot = Bot.objects.get(token=token)

        markaz = Markaz.objects.get(id=bot.markaz.id)

        chat = Chat.objects.get_or_create(user_chat_id=chat_id, markaz_id=markaz.id, defaults={'title': first_name}, )

        message = Message.objects.create(chat_id=chat[0].id, text=text)

        return Response({'result': 'ok'}, status=201)


class SendReplyMessage(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(methods=['post'], detail=False)
    def send(self, request):
        chat_id = request.POST['chat_id']
        text = request.POST['text']
        user_chat_id = request.POST['user_chat_id']

        chat = Chat.objects.get(id=chat_id)
        TOKEN = chat.markaz.bot_set.all()[0].token

        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={user_chat_id}&text={text}")
        xabar = Message.objects.create(chat_id=chat_id, text=text, own=True)
        xabar = self.get_serializer_class()(xabar)

        return Response(xabar.data, status=201)


class ChatViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz_id']
        data = []
        chats = Chat.objects.filter(markaz_id=markaz_id)
        bot = Bot.objects.get(markaz_id=markaz_id)
        for chat in chats:
            data.append(
                {'id': chat.id,
                 'title': chat.title,
                 'user_chat_id': chat.user_chat_id,
                 'markaz_id': chat.markaz.id,
                 'bot_token': bot.token
                 }
            )

        return Response(data, status=200)


class MessageViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(methods=['get'], detail=False)
    def get_messages(self, request):
        chat_id = request.GET['chat_id']

        messages = Message.objects.filter(chat_id=chat_id)

        messages = self.get_serializer_class()(messages, many=True)

        return Response(messages.data, status=200)


def get_company(request):
    token = request.GET['token']

    bot = Bot.objects.get(token=token)

    markaz = {
        'name': bot.markaz.name,
        'id': bot.markaz.id
    }

    return JsonResponse(markaz)


def save_message(user_tg_id, first_name, text, own, token):
    bot = Bot.objects.get(token=token)
    markaz_id = bot.markaz.id
    try:
        chat = Chat.objects.get(user_chat_id=user_tg_id, markaz_id=markaz_id)
        message = Message.objects.create(chat_id=chat.id, text=text, own=own)
    except:
        chat = Chat.objects.create(title=first_name, user_chat_id=user_tg_id, markaz_id=markaz_id)
        message = Message.objects.create(chat_id=chat.id, text=text, own=own)
        print(message, 'done...')


def get_user_tg_ids(request):
    user_tg_ids = Chat.objects.values_list('user_chat_id')
    print(user_tg_ids)
    chats = Chat.objects.all()
    chat_ids = []
    for chat in chats:
        chat_ids.append(chat.user_chat_id)
    ids = list(user_tg_ids)
    print('ids', ids)
    return JsonResponse({"user_tg_ids": chat_ids})


def chats(request):
    return render(request, 'index.html')


def room(request, chat_id):
    return render(request, 'websocket.html')


def get_token(request):
    markaz_id = request.GET['markaz_id']
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", markaz_id)
    bot = Bot.objects.get(markaz_id=markaz_id)
    print(bot.token)
    return JsonResponse({"token": bot.token})
