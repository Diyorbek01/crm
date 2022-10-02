from datetime import datetime
from itertools import chain

from django.db.models import query, Sum
from django.db.models.query_utils import Q
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from group.serializers import GroupSerializer
from payment.models import *
from payment.serializers import *


class PaymentViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz']
        payment = Payment.objects.filter(markaz_id=markaz_id)
        data = self.get_serializer_class()(payment, many=True)

        return Response(data.data, status=200)

    @action(methods=['get'], detail=False)
    def filterstudent(self, request):
        markaz_id = request.GET['markaz']
        student_id = request.GET['student_id']
        payment = Payment.objects.filter(markaz_id=markaz_id, learner=student_id)
        data = self.get_serializer_class()(payment, many=True)

        return Response(data.data, status=200)

    @action(methods=['post'], detail=False)
    def add(self, request):
        payment = request.data
        markaz = payment['markaz']
        staff = payment['staff']

        serializer = PaymentSerializer(data=payment)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        history = History.objects.create(markaz_id=markaz, user=staff, did="Yangi to'lov yaratdi")
        return Response(serializer.errors, status=203)

    @action(methods=['get'], detail=False)
    def filter(self, request):
        r = request.GET
        from_date = r['from_date']
        to_date = r['to_date']
        markaz_id = r['markaz']
        staff = r['staff']
        payments = Payment.objects.filter(date__gte=from_date, date__lte=to_date, markaz_id=markaz_id)
        history = History.objects.create(markaz_id=markaz_id, user=staff, did="To'lov bo'limida filter qildi")

        data = self.get_serializer_class()(payments, many=True)
        return Response(data.data, status=200)

    @action(methods=['get'], detail=False)
    def filter_statistic(self, request):
        res = request.GET
        markaz = res['markaz']
        from_date = res['from_date']
        to_date = res['to_date']
        payments = Payment.objects.filter(markaz_id=markaz, create_at__gte=from_date,
                                          create_at__lte=to_date)
        expense = Expense.objects.filter(markaz_id=markaz, date__gte=from_date, date__lte=to_date)

        total_expense = 0
        total = 0
        for i in payments:
            total = total + i.amount
        for i in expense:
            total_expense = total_expense + i.amount
        income = total - total_expense

        data = {
            "total": total,
            "total_expense": total_expense,
            "income": income,
        }
        return Response(data, status=200)

    @action(methods=['get'], detail=False)
    def statistic(self, request):
        res = request.GET
        markaz = res['markaz']
        payments = Payment.objects.filter(markaz_id=markaz)
        expense = Expense.objects.filter(markaz_id=markaz)
        total_expense = 0
        total = 0
        for i in payments:
            total = total + i.amount
        for i in expense:
            total_expense = total_expense + i.amount
        income = total - total_expense

        group_pay = Group.objects.raw("""SELECT  gr.id as id, gr.name as gr_name,
course.id as course_id, course.name as course_name, course.price as price, count(student.id) as students,
count(student.id)*course.price as total_pay
FROM group_group as gr


left join main_course as course on gr.course_id=course.id
left join students_students_group as student on student.group_id=gr.id
LEFT JOIN students_students as sstudent on sstudent.id = student.id
WHERE sstudent.payment_status = 1 and gr.markaz_id = %s

GROUP by gr.id""", [markaz])

        more_pay = Group.objects.raw('''SELECT  gr.id as id, gr.name as gr_name,
course.id as course_id, course.name as course_name, course.price as price, count(student.id) as students,
count(student.id)*course.price as total_pay
FROM group_group as gr


left join main_course as course on gr.course_id=course.id
left join students_students_group as student on student.group_id=gr.id
LEFT JOIN students_students as sstudent on sstudent.id = student.id
WHERE gr.markaz_id = %s

GROUP by gr.id''', [markaz])

        total_pay = 0
        for i in group_pay:
            total_pay = total_pay + i.total_pay

        total_group_payment = Group.objects.raw('''SELECT  gr.id as id, gr.name as gr_name,
course.id as course_id, course.name as course_name, course.price as price, count(student.id) as students,
count(student.id)*course.price as total_salary
FROM group_group as gr


left join main_course as course on gr.course_id=course.id
left join students_students_group as student on student.group_id=gr.id
WHERE gr.markaz_id = %s

GROUP by gr.id''', [markaz])

        total_payment = 0
        for i in total_group_payment:
            total_payment = total_payment + i.total_salary

        paid_group = []
        for i in group_pay:
            paid_group.append(i.id)

        unpaid = total_payment - total_pay
        unpaid_percent = unpaid * 100 / total_payment
        paid_percent = 100 - unpaid_percent
        data = {
            "total": total,
            "total_expense": total_expense,
            "income": income,
            "total_payment_group": total_payment,
            "total_paid_group": total_pay,
            "total_unpaid_group": unpaid,
            "unpaid_percent": round(unpaid_percent),
            "paid_percent": round(paid_percent),
        }
        return Response(data, status=200)

    @action(methods=['get'], detail=False)
    def group_statistic(self, request):
        groups = Group.objects.all()
        group = []
        for gr in groups:
            paid_student = Students.objects.filter(group=gr.id, payment_status=1).count()
            unpaid_student = Students.objects.filter(group=gr.id, payment_status=2).count()
            total_student = Students.objects.filter(group=gr.id).count()
            summa = gr.course.price * paid_student
            if paid_student > 0:
                percent = paid_student * 100 / total_student
            else:
                percent = 0
            group.append({
                "gr_id": gr.id,
                "gr_name": gr.name,
                "number_paid_student": paid_student,
                "number_unpaid_student": unpaid_student,
                "number_total_student": total_student,
                "summa": summa,
                "percent": round(percent),
            })
        return Response(group, status=200)


@api_view(['post'])
def edit(request, pk):
    staff = request.data['staff']
    markaz_id = request.data['markaz']
    student = Payment.objects.get(id=pk)
    serializer = PaymentSerializer(instance=student, data=request.data)

    if serializer.is_valid():
        serializer.save()
        history = History.objects.create(markaz_id=markaz_id, user=staff, did="To'lov ma'lumotlarini o'zgartirdi")

    return Response(serializer.data)


class ExpenseViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz']

        expense = Expense.objects.filter(markaz_id=markaz_id)
        data = []
        for i in expense:
            if i.category == None:
                data.append({
                    "category_name": 'Hodimlar uchun oylik',
                    "amount": i.amount,
                    "recipient": i.recipient,
                    "name": i.name,
                    "date": i.create_at,
                })
            else:
                data.append({
                    "category_name": i.category.name,
                    "amount": i.amount,
                    "recipient": i.recipient,
                    "name": i.name,
                    "date": i.date,
                })

        # data = self.get_serializer_class()(expence, many=True)

        return Response(data, status=200)

    @action(methods=['get'], detail=False)
    def filter(self, request):
        r = request.GET
        from_date = r['from_date']
        to_date = r['to_date']
        markaz_id = r['markaz']
        staff = r['staff']

        payments = Expense.objects.filter(date__gte=from_date, date__lte=to_date, markaz_id=markaz_id)
        history = History.objects.create(markaz_id=markaz_id, user=staff, did="Harajat bo'limida filter qildi")

        data = self.get_serializer_class()(payments, many=True)

        return Response(data.data, status=200)

    @action(methods=['post'], detail=False)
    def post(self, request):
        expense = request.data

        markaz = expense['markaz']
        staf = expense['staff']

        serializer = ExpenseSerializer(data=expense)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        history = History.objects.create(markaz_id=markaz, user=staf, did="Yangi harajat yaratdi")
        return Response(serializer.errors, status=222)

    @action(methods=['get'], detail=False)
    def get_static(self, request):
        markaz_id = request.GET['markaz']

        payment = Payment.objects.filter(markaz=markaz_id).order_by('create_at')
        expense = Expense.objects.filter(markaz=markaz_id).order_by('create_at')

        expenses = []
        payments = []
        for p in payment:
            # print(p.learner.group.name)
            payments.append({
                "id": p.id,
                "name": p.learner.name,
                "student_id": p.learner.id,
                "plusamount": p.amount,
                "description": p.comment,
                "group": p.learner.group.name,
                "group_id": p.learner.id,
                "date": str(p.create_at)
            })
        for e in expense:
            expenses.append({
                "id": e.id,
                "name": e.recipient,
                "minusamount": e.amount,
                "description": e.name,
                "date": str(e.create_at)
            })
        data = expenses + payments
        sorted_date = sorted(data, key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))

        return Response(sorted_date, status=200)

    @action(methods=['get'], detail=False)
    def get_total_statistic(self, request):
        markaz = request.GET['markaz']
        payment = Payment.objects.filter(markaz=markaz)
        expense = Expense.objects.filter(markaz=markaz)
        data = []
        for i in payment:
            data.append({
                "payment_amount": i.amount,
                "date": str(i.create_at).replace('-', ', ')
            })
        for e in expense:
            data.append({
                "expense_amount": e.amount,
                "date": str(e.date).replace('-', ', ')
            })

        return Response(data)

    @action(methods=['get'], detail=False)
    def filter_total_statistic(self, request):

        markaz = request.GET['markaz']
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        payment = Payment.objects.filter(markaz_id=markaz, create_at__gte=from_date,
                                         create_at__lte=to_date)
        expense = Expense.objects.filter(markaz_id=markaz, create_at__gte=from_date, create_at__lte=to_date)
        data = []
        for i in payment:
            data.append({
                "payment_amount": i.amount,
                "date": i.create_at
            })
        for e in expense:
            data.append({
                "expense_amount": e.amount,
                "date": e.create_at,
            })

        return Response(data)


class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz']
        category = Category.objects.filter(markaz_id=markaz_id)

        data = self.get_serializer_class()(category, many=True)

        return Response(data.data, status=200)

    @action(methods=['post'], detail=False)
    def post(self, request):
        category = request.data

        markaz = category['markaz']
        staff = category['staff']
        serializer = CategorySerializer(data=category)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        history = History.objects.create(markaz_id=markaz, user=staff, did="Yangi harajat bo'limi yaratdi")

        return Response(serializer.errors, status=222)

    @action(methods=['post'], detail=False)
    def delete(self, request):
        data = request.data
        markaz = data['markaz']
        staff = data['staff']
        category_id = data['category_id']
        history = History.objects.create(markaz_id=markaz, user=staff, did="Xarajat bo'lim ma'lumotini o'chirdi")

        category = Category.objects.get(id=category_id)
        category.typ = "Delete"
        category.save()
        return Response({"id": category.id}, status=200)


class SalaryViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Salary.objects.all()
    serializer_class = SalaryPostSerializer
    serializer_clas = GroupSerializer

    @action(methods=['get'], detail=False)
    def all(self, request):
        markaz_id = request.GET['markaz']
        salarys = Salary.objects.filter(markaz_id=markaz_id)

        data = []
        for i in salarys:
            data.append({
                "mentor_id": i.mentor.id,
                "mentor_name": i.mentor.full_name,
                "amount": i.amount,
                "status": i.status,
                "create_at": i.create_at,
            })

        # data = self.get_serializer_class()(salarys, many=True)

        return Response(data, status=200)

    @action(methods=['get'], detail=False)
    def get(self, request):
        markaz_id = request.GET['markaz']
        salarys = Salary.objects.filter(markaz_id=markaz_id)

        data = self.get_serializer_class()(salarys, many=True)

        return Response(data.data, status=200)

    @action(methods=['post'], detail=False)
    def single(self, request):
        category = request.data
        # print(category)
        amount = category['amount']
        status = category['status']
        type = category['type']
        mentor = category['mentor']
        salar = Salary.objects.all()
        val = []
        if salar:
            for sal in Salary.objects.all():
                if int(mentor) == sal.mentor.id:
                    val.append(1)
            if val and val[0] == 1:
                salary = Salary.objects.get(mentor_id=mentor)
                salary.amount = amount
                salary.status = status
                salary.type = type
                salary.save()
                data = {
                    "amount": amount,
                    "status": str(status),
                    "type": type,
                    "full_name": salary.mentor.full_name,
                    "teacher_id": salary.mentor.id,
                }
            else:
                result = Salary.objects.create(markaz_id=category["markaz"], amount=amount, status=status, type=type,
                                               mentor_id=mentor)
                history = History.objects.create(markaz_id=category["markaz"], user=category["staff"],
                                                 did="Oylik to'ladi")
                data = {
                    "amount": amount,
                    "status": str(status),
                    "type": type,
                    "full_name": result.mentor.full_name,
                }

            return Response(data, status=201)

        else:
            result = Salary.objects.create(markaz_id=category["markaz"], amount=amount, status=status,
                                           type=type, mentor_id=mentor)
            history = History.objects.create(markaz_id=category["markaz"], user=category["staff"],
                                             did="Oylik yaratdi")
            data = {
                "amount": amount,
                "status": str(status),
                "type": type,
                "full_name": result.mentor.full_name,
            }
            return Response(data, status=201)

    @action(methods=['post'], detail=False)
    def everybody(self, request):
        salary = request.data
        markaz = salary['markaz']
        amount = salary['amount']
        status = salary['status']
        teache = salary['teacher']
        type = salary['type']

        mentors = Salary.objects.all()
        if teache == 'Teacher':
            staff = Staff.objects.filter(role=teache)
        elif teache == 'Staff':
            staff = Staff.objects.filter(~Q(role='Teacher'))

        teac = []
        for staf in staff:
            teac.append(staf.id)
        da = []
        update = []
        if mentors:
            for prof in mentors:
                mentor_id = prof.mentor.id
                for teacher in staff:

                    if mentor_id == teacher.id:
                        update.append(mentor_id)
            create = list(set(teac) - set(update))
            for upda in update:
                salary = Salary.objects.get(mentor_id=upda)
                salary.amount = amount
                salary.status = status
                salary.type = type
                salary.save()
                data = {
                    "markaz": markaz,
                    "amount": amount,
                    "status": str(status),
                    "type": type,
                    "full_name": salary.mentor.full_name
                }
                da.append(data)
            for cre in create:
                result = Salary.objects.create(markaz_id=markaz, mentor_id=cre, amount=amount, status=status,
                                               type=type)
                data = {
                    "markaz": markaz,
                    "amount": amount,
                    "status": str(status),
                    "type": type,
                    "full_name": result.mentor.full_name,
                }
                da.append(data)
        else:
            for teach in teac:
                result = Salary.objects.create(markaz_id=markaz, mentor_id=teach, amount=amount, status=status,
                                               type=type)
                data = {
                    "markaz": markaz,
                    "amount": amount,
                    "status": status,
                    "type": type,
                    "full_name": result.mentor.full_name,
                }
                da.append(data)

        return Response(da, status=201)

    @action(methods=['get'], detail=False)
    def summa(self, request):
        markaz_id = request.GET['markaz']
        salarys = Staff.objects.raw('''
        SELECT teacher.id as id, IFNULL(teacher.full_name,0) as teacher_name, IFNULL(gr.id,0) as gr_id, IFNULL(gr.name,0) as gr_name, 
IFNULL(course.price,0) as gr_price, IFNULL(count(student.id),0) as students, IFNULL(count(student.id)*course.price,0) as total_salary, 
salary.type as status, IFNULL(salary.amount,0) as amount,teacher.role as role,
CASE
    WHEN salary.type = 1 THEN IFNULL(count(student.id)*course.price*salary.amount/100,0)
    WHEN salary.type = 2 THEN IFNULL(count(student.id)*salary.amount,0)
    ELSE IFNULL(salary.amount,0)
END AS salaryy
from main_staff as teacher
LEFT join group_group as gr on teacher.id = gr.teacher_id
LEFT join main_course as course on course.id = gr.course_id
left join students_students_group as student on student.group_id=gr.id
left join payment_salary as salary on salary.mentor_id=teacher.id

WHERE teacher.markaz_id=%s and teacher.role = 'Teacher'
GROUP by gr.id
''', [markaz_id])
        lastdate = Expense.objects.filter(markaz_id=markaz_id, recipient='Hodimlar', name='Oylik').first()
        data = []
        for i in salarys:
            if lastdate == None:
                data.append({
                    "teacher_id": i.id,
                    "teacher_name": i.teacher_name,
                    "gr_name": i.gr_name,
                    "gr_price": i.gr_price,
                    "number_students": i.students,
                    "role": i.role,
                    "total_salary": i.total_salary,
                    "status": i.status,
                    "amount": i.amount,
                    "salary": i.salaryy,
                    "lastdate": "birinchi"
                })
            else:
                data.append({
                    "teacher_id": i.id,
                    "teacher_name": i.teacher_name,
                    "gr_name": i.gr_name,
                    "gr_price": i.gr_price,
                    "number_students": i.students,
                    "role": i.role,
                    "total_salary": i.total_salary,
                    "status": i.status,
                    "amount": i.amount,
                    "salary": i.salaryy,
                    "lastdate": lastdate.create_at
                })

        againwork = Salary.objects.filter(~Q(mentor__role="Teacher"),markaz_id=markaz_id)

        for i in againwork:
            data.append({
                "teacher_id": i.mentor.id,
                "teacher_name": i.mentor.full_name,
                "role": i.mentor.role,
                "salary": i.amount,
            })

        return Response(data, status=200)

    @action(methods=['post'], detail=False)
    def paysalary(self, request):
        data = request.data
        salary = data['salary']
        markaz = data['markaz']
        staff = data['staff']
        result = Expense.objects.create(markaz_id=markaz, amount=salary, name="Oylik", recipient="Hodimlar")
        history = History.objects.create(markaz_id=markaz, user=staff, did="Hodimlar uchun oylik yaratildi")
        # dat = []
        # dat.append("")
        return Response("created", status=201)

    @action(methods=['post'], detail=False)
    def delete(self, request):
        data = request.data
        markaz = data['markaz']
        staff = data['staff']
        expense_id = data['expense_id']
        history = History.objects.create(markaz_id=markaz, user=staff, did="Xarajat ma'lumotini o'chirdi")

        expensed = Expense.objects.get(id=expense_id)
        expensed.typ = "Delete"
        expensed.save()
        return Response("Deleted", status=200)
