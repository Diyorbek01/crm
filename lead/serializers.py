from rest_framework import serializers
from .models import *


class LeadSerializer(serializers.ModelSerializer):
    name_course = serializers.SerializerMethodField('get_course')
    name_category = serializers.SerializerMethodField('get_category')
    id_category = serializers.SerializerMethodField('get_category_id')
    name_status = serializers.SerializerMethodField('get_status')
    id = serializers.SerializerMethodField('get_id')

    def get_course(self, result):
        teacher_id = getattr(result, "course_id")
        result = Lead.objects.filter(course_id=teacher_id)
        for i in result:
            name = i.course.name
            return name

    def get_category(self, result):
        teacher_id = getattr(result, "where_id")
        result = Lead.objects.filter(where=teacher_id)
        for i in result:
            name = i.where.name
            return name

    def get_category_id(self, result):
        teacher_id = getattr(result, "where_id")
        result = Lead.objects.filter(where=teacher_id)
        for i in result:
            name = i.where.id
            return name

    def get_status(self, result):
        teacher_id = getattr(result, "status")
        result = Lead.objects.filter(status=teacher_id)
        for i in result:
            name = i.status
            return name

    def get_id(self, result):
        teacher_id = getattr(result, "id")
        # result = Lead.objects.filter(status=teacher_id)
        # for i in result:
        #     name = i.status
        return teacher_id

    class Meta:
        model = Lead
        # fields = ['id','markaz','status','name_category','name_course','name_status']
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'
