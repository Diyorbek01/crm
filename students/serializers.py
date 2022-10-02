from group.models import Group
from lead.models import Lead, Place
from main.serializers import MarkazSerializer, CourseSerializer
from students import models
from django.contrib.auth.models import User
from rest_framework import serializers

from students.models import Students


class SimpleGroupSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = models.Group
        fields = '__all__'


class StudentsSerializer(serializers.ModelSerializer):
    name_group = serializers.SerializerMethodField('get_group')
    name_lead = serializers.SerializerMethodField('get_lead')

    def get_group(self, result):
        student_id = getattr(result, "test")
        result = Group.objects.get(id=student_id)
        return [result.name]
    def get_lead(self, result):
        student_id = getattr(result, "lead_category")
        result = Place.objects.get(name=student_id).name
        return result

    class Meta:
        model = models.Students
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attendance
        fields = '__all__'


class StudentGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Attendance
        fields = '__all__'

