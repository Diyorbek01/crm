from rest_framework import serializers
from .models import *


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class MarkazSerializer(serializers.ModelSerializer):
    class Meta:
        model = Markaz
        fields = '__all__'


class CourseSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    price = serializers.IntegerField()
    duration = serializers.FloatField()
    photo = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    description = serializers.CharField(max_length=150)

    class Meta:
        model = Course
        fields = '__all__'




class CourseCategorySerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = CourseCategory
        fields = '__all__'


class CoursePlanSerializer(serializers.ModelSerializer):
    markaz = MarkazSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    category = CourseCategorySerializer(read_only=True)

    class Meta:
        model = CoursePlan
        fields = '__all__'


class CourseGraduateSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    # category = CourseCategorySerializer(read_only=True)

    class Meta:
        model = CourseGraduate
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    markaz = MarkazSerializer(read_only=True)

    class Meta:
        model = History
        fields = '__all__'


class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
