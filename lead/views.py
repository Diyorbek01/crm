from django.db.models.query_utils import Q
from lead.serializers import LeadSerializer, PlaceSerializer
from rest_framework import views, viewsets

from main.models import History
from students.models import Students
from .models import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view


class LeadFormViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz']

        places = Lead.objects.filter(Q(markaz_id=markaz_id) | Q(markaz_id=None),
                                     Q(status="Yangi") | Q(status="Aloqada"))

        data = self.get_serializer_class()(places, many=True)
        return Response(data.data)

    @action(methods=['get'], detail=False)
    def links(self, request):
        markaz_id = request.GET['markaz']
        url = request.GET['url']

        category = Place.objects.filter(markaz_id=markaz_id)
        data = []
        for i in category:
            data.append({
                "id": i.id,
                "name": i.name,
                "link": f"{url}/links#{i.name}",
            })

        return Response(data)

    @action(methods=['post'], detail=False)
    def post(self, request):
        where = request.data
        markaz_id = request.data['markaz']
        staff = request.data['staff']
        serializer = LeadSerializer(data=where)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        history = History.objects.create(markaz_id=markaz_id, user=staff, did="Yangi lid yaratdi")

        return Response(serializer.errors, status=400)

    @action(methods=['post'], detail=False)
    def postlink(self, request):
        data = request.data
        print(data)
        markaz_id = request.data['markaz']
        full_name = request.data['name']
        phone = request.data['phone']
        description = request.data['comment']
        course = request.data['course']
        where = request.data['where']
        plac = str(where).replace('#', '')
        course_id = Course.objects.get(markaz_id=markaz_id, name=course)
        print(plac)
        place = Place.objects.get(markaz_id=markaz_id, name=plac)
        print(place.id)

        result = Lead.objects.create(
            markaz_id=markaz_id,
            full_name=full_name,
            phone=phone,
            description=description,
            course=course_id,
            where_id=place.id
        )

        return Response("Created", status=201)

    @action(methods=['get'], detail=False)
    def statistic(self, request):
        markaz = request.GET['markaz']
        process_student = Students.objects.filter(markaz=markaz, type=1).count()
        new_lead = Lead.objects.filter(markaz=markaz, status='Yangi').count()
        contact_lead = Lead.objects.filter(status='Aloqada').count()
        delete_lead = Lead.objects.filter(status='Delete').count()
        data = {
            "process_student": process_student,
            "new_lead": new_lead,
            "contact_lead": contact_lead,
            "delete_lead": delete_lead,
        }

        return Response(data, status=200)

    @action(methods=['get'], detail=False)
    def placestatistic(self, request):
        markaz = request.GET['markaz']
        place = Place.objects.filter(markaz=markaz)
        data = []
        for p in place:
            lead_number = Lead.objects.filter(~Q(status="Delete"), markaz=markaz, where=p.id).count()

            data.append({
                "category_name": p.name,
                "category_id": p.id,
                "category_number": lead_number
            })
        v = 0
        for d in data:
            v += d['category_number']

        newdata = []
        for k in data:
            result = k['category_number'] * 100 / v
            newdata.append({
                "category_name": k["category_name"],
                "category_id": k["category_id"],
                "category_number": k["category_number"],
                "percent": round(result),
            })

        return Response(newdata, status=200)

    @action(methods=['post'], detail=False)
    def edit(self, request):
        where = request.data
        markaz_id = request.data['markaz']
        course = where['item']['name_course']
        category = where['item']['name_category']
        name = where['item']['full_name']
        description = where['item']['description']
        phone = where['item']['phone']
        staff = request.data['staff']
        status = request.data['status']
        id = where.pop('id')
        stat = where.pop('status')
        lead = Lead.objects.get(id=id)
        lead.status = stat
        lead.save()
        history = History.objects.create(markaz_id=markaz_id, user=staff, did="Lid holatini o'zgartirdi")

        data = {
            "status": stat,
            "name_course": course,
            "name_category": category,
            "full_name": name,
            "description": description,
            "phone": phone,
            "id": id,
        }
        return Response(data, status=201)

    @action(methods=['post'], detail=False)
    def addgroup(self, request):
        student = request.data
        markaz = student['markaz']
        name = student['full_name']
        phone = student['phone']
        group_id = student['group']
        staff = student['staff']
        result = Students.objects.create(markaz_id=markaz, name=name, phone=phone, )
        history = History.objects.create(markaz_id=markaz, user=staff, did="Lid ni guruhga qo'shdi")

        result.group.set(group_id)
        result.save()
        id = student.pop('id')
        lead = Lead.objects.get(id=id)
        lead.status = "Delete"
        lead.save()
        return Response("created", status=201)


@api_view(['post'])
def edit(request, pk):
    staff = request.data['staff']
    markaz_id = request.data['markaz']
    student = Lead.objects.get(id=pk)
    serializer = LeadSerializer(instance=student, data=request.data)

    if serializer.is_valid():
        serializer.save()
        history = History.objects.create(markaz_id=markaz_id, user=staff, did="Lid ma'lumotlarini o'zgartirdi")

    return Response(serializer.data)


class PlaceViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz']

        places = Place.objects.filter(Q(markaz_id=markaz_id) | Q(markaz_id=None))

        data = self.get_serializer_class()(places, many=True)
        return Response(data.data)

    @action(methods=['post'], detail=False)
    def post(self, request):
        place = request.data
        markaz_id = request.data['markaz']
        staff = request.data['staff']

        serializer = PlaceSerializer(data=place)
        if serializer.is_valid():
            serializer.save()
            history = History.objects.create(markaz_id=markaz_id, user=staff, did="Yangi lid uchun bo'lim  yaratdi")

            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
