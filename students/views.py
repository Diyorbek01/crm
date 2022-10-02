from django.http import JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from group.models import Group
from main.models import Markaz, History
from students.models import Students, Attendance
from students.serializers import StudentsSerializer, AttendanceSerializer, StudentGroupSerializer


class StudentsViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz']
        students = Students.objects.filter(markaz_id=markaz_id, type="Appear")

        student = []
        for st in students:
            student.append({
                "id": st.id,
                "name_group": [x.name for x in st.group.all()],
                "id_group": [x.id for x in st.group.all()],
                "name_lead": st.lead_category.name,
                "id_lead": st.lead_category.id,
                "name": st.name,
                "phone": st.phone,
                "birthday": st.birthday,
                "gender": st.gender,
                "photo": '/media/' + st.photo.name,
                "comment": st.comment,
                "parents_phone": st.parents_phone,
                "telegram": st.telegram,
                "address": st.address,
                # "test": st.test,
                "type": st.type,
                "payment_status": st.payment_status,
                "create_at": st.create_at,
                "update_at": st.update_at,
            })

        return Response(student)

    @action(methods=['post'], detail=False)
    def post(self, request):
        post = request.data
        print(post)
        serializer = StudentsSerializer(data=post)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)

        return JsonResponse(serializer.errors, status=400)

    @action(methods=['post'], detail=False)
    def addgroup(self, request):
        student_data = request.data
        markaz = student_data['markaz']
        student_id = student_data['student_id']
        group_id = student_data['group_id']
        student = Students.objects.get(markaz_id=markaz, id=student_id)
        student.group.add(group_id)
        student.save()

        return Response("created", status=201)

    @action(methods=['post'], detail=False)
    def deletegroup(self, request):
        student_data = request.data
        markaz = student_data['markaz']
        student_id = student_data['student_id']
        group_id = student_data['group_id']
        student = Students.objects.get(markaz_id=markaz, id=student_id)
        student.group.remove(group_id)
        student.save()

        return Response({"id": student.id}, status=201)

    @action(methods=['post'], detail=False)
    def delete(self, request):
        data = request.data
        print(data)
        markaz = data['markaz']
        staff = data['staff']
        student_id = data['student_id']
        history = History.objects.create(markaz_id=markaz, user=staff, did="O'quvchi ma'lumotini o'chirdi")

        student = Students.objects.get(id=student_id)
        student.type = "Delete"
        student.save()
        return Response({"id": student.id}, status=200)


@api_view(['post'])
def edit(request):
    print(request.data)
    staff = request.data['staff']
    markaz_id = request.data['markaz']
    id = request.data['id']
    name = request.data['name']
    lead_category = request.data['lead_category']
    phone = request.data['phone']
    birthday = request.data['birthday']
    # photo = request.FILES['photo']
    gender = request.data['gender']
    image = request.data['photo']
    comment = request.data['comment']
    parents_phone = request.data['parents_phone']
    address = request.data['address']
    telegram = request.data['telegram']
    student = Students.objects.get(id=id)
    if image == 'hello':
        # student.photo = photo,
        student.markaz_id = markaz_id
        student.phone = phone
        student.gender = gender
        student.address = address
        student.telegram = telegram
        student.parents_phone = parents_phone
        student.comment = comment
        # student.group.add(group)
        student.birthday = birthday
        student.lead_category.id = lead_category
        student.name = name
        student.save()
    else:
        student.photo = request.FILES['photo']
        student.markaz_id = markaz_id
        student.phone = phone
        student.address = address
        student.telegram = telegram
        student.parents_phone = parents_phone
        student.comment = comment
        # student.group = group
        student.gender = gender
        student.birthday = birthday
        student.lead_category.id = lead_category
        student.name = name
        student.save()
    data = {
        'photo': '/media/' + student.photo.name,
        'phone': student.phone,
        # "payment_status": student.payment_status,
        'gender': student.gender,
        'address': student.address,
        'telegram': student.telegram,
        'parents_phone': student.parents_phone,
        'comment': student.comment,
        "id_group": [x.id for x in student.group.all()],
        "name_group": [x.name for x in student.group.all()],
        "birthday": student.birthday,
        'name': student.name,
        "lead_category": student.lead_category.name
    }

    history = History.objects.create(markaz_id=markaz_id, user=staff, did="O'quvchi ma'lumotlarini o'zgartirdi")
    return Response(data)


class AttendanceViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz']
        group_id = request.GET['group']
        students = Students.objects.filter(group=group_id)
        attandance = Attendance.objects.filter(markaz_id=markaz_id, group=group_id)
        student = []
        for i in attandance:
            if not i.student.name in student:
                student.append(i.student.name)

        data = self.get_serializer_class()(attandance, many=True)
        return Response(data.data)

    @action(methods=['post'], detail=False)
    def post(self, request):
        post = request.data
        print(post)
        data = []
        for i in post:
            markaz = i['markaz']
            action = i['action']
            student = i['student']
            # date = i['date']
            group = i['group']

            attendance = Attendance.objects.create(
                action=action,
                markaz_id=markaz,
                student_id=student,
                # date=date,
                group_id=group,
            )
            serializer = self.get_serializer_class()(attendance)
            data.append({
                "action": attendance.action,
                "student": attendance.student.id,
                "date": attendance.date,
                "group": attendance.group.id,
            })
        return Response(data, status=201)


class AddGroupViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer

    @action(methods=['post'], detail=False)
    def post(self, request):
        post = request.data
        posts = post.dict()
        student_id = posts["student"]
        group_id = posts["group"]
        serializer = StudentsSerializer(data=posts)

        student = Students.objects.get(id=student_id)
        student.group.set(group_id)
        student.save()
        return Response(serializer.data)


class StudentsAttandanceViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Students.objects.all()
    serializer_class = StudentGroupSerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz']
        group_id = request.GET['group']
        students = Students.objects.filter(markaz_id=markaz_id, group=group_id)
        student = []
        for st in students:
            student.append({
                "id": st.id,
                # "name_group": [x.name for x in st.group.all()],
                # "id_group": [x.id for x in st.group.all()],
                "name_lead": st.lead_category.name,
                "name": st.name,
                "phone": st.phone,
                "birthday": st.birthday,
                "gender": st.gender,
                "photo": '/media/' + st.photo.name,
                "comment": st.comment,
                "parents_phone": st.parents_phone,
                "telegram": st.telegram,
                "address": st.address,
                # "test": st.test,
                "type": st.type,
                "payment_status": st.payment_status,
                "create_at": st.create_at,
                "update_at": st.update_at,
            })

        return Response(student)
