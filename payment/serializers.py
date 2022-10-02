from group.models import Group
from main.models import Staff, Course
from main.serializers import MarkazSerializer
from payment import models
from rest_framework import serializers

from payment.models import Salary, Expense, Payment
from students.models import Students


class PaymentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField('get_mentor')
    total_month = serializers.SerializerMethodField('get_month')
    group_name = serializers.SerializerMethodField('get_group')

    def get_mentor(self, result):
        learner_id = getattr(result, "learner")
        result = Payment.objects.filter(learner_id=learner_id)
        for i in result:
            name = i.learner.name
            return name

    def get_month(self, result):
        student_id = getattr(result, "learner")
        result = Students.objects.get(id=student_id.id)
        group = result.group.all()
        for i in group:
            res = int(i.course.duration)
            return res

    def get_group(self, result):
        group_id = getattr(result, "group")
        result = Payment.objects.filter(group=group_id)
        for i in result:
            name = i.group.name
            return name

    class Meta:
        model = models.Payment
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    # category_name = serializers.SerializerMethodField('get_category')
    #
    # def get_category(self, result):
    #     category_id = getattr(result, "category")
    #     result = Expense.objects.filter(category_id=category_id)
    #     for i in result:
    #         name = i.category.name
    #         return name

    class Meta:
        model = models.Expense
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class SalaryPostSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField('get_mentor')
    role = serializers.SerializerMethodField('get_role')

    def get_mentor(self, result):
        teacher_id = getattr(result, "mentor_id")
        mentor_id = Staff.objects.get(id=teacher_id)
        name = mentor_id.full_name
        return name

    def get_role(self, result):
        teacher_id = getattr(result, "mentor_id")
        mentor_id = Staff.objects.get(id=teacher_id)
        name = mentor_id.role
        return name

    class Meta:
        model = models.Salary
        fields = '__all__'
