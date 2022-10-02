from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView

from group.models import Group
from group.serializers import GroupSerializer, GroupGetSerializer
from main.models import History


class GroupViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Group.objects.all()

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz = request.GET['markaz']
        questions = Group.objects.filter(markaz_id=markaz)
        serailizer = GroupSerializer(questions, many=True)
        return Response(serailizer.data, status=200)

    @action(methods=['post'], detail=False)
    def changetype(self, request):
        markaz = request.data['markaz']
        staff = request.data['staff']
        group_id = request.data['group_id']

        group = Group.objects.get(markaz_id=markaz, id=group_id)
        group.typ = "Jarayonda"
        group.save()
        data = {
            'id': group.id,
            'typ': group.typ,
        }
        history = History.objects.create(markaz_id=markaz, user=staff, did="Guruh holatini o'zgartirdi")
        return Response(data, status=201)

    @action(methods=['post'], detail=False)
    def post(self, request):
        data = request.data
        markaz = data['markaz']
        staff = data['staff']
        serializer = GroupSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            history = History.objects.create(markaz_id=markaz, user=staff, did="Yangi guruh yaratdi")
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(methods=['post'], detail=False)
    def delete(self, request):
        data = request.data
        markaz = data['markaz']
        staff = data['staff']
        group_id = data['group_id']
        history = History.objects.create(markaz_id=markaz, user=staff, did="Guruhni o'chirdi")

        group = Group.objects.get(id=group_id)
        group.typ = "Ochirilgan"
        group.save()
        return Response({"id": group.id}, status=200)


@api_view(['post'])
def edit(request, pk):
    staff = request.data['staff']
    markaz_id = request.data['markaz']
    student = Group.objects.get(id=pk)
    serializer = GroupSerializer(instance=student, data=request.data)

    if serializer.is_valid():
        serializer.save()
        history = History.objects.create(markaz_id=markaz_id, user=staff, did="Guruh ma'lumotlarini o'zgartirdi")

    return Response(serializer.data)
