from django.contrib import admin
from .models import *



@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'markaz', 'learner','amount','comment','type')
    list_display_links = ('id', 'markaz', 'learner','amount','comment','type')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','markaz', 'category','amount','date','recipient')
    list_display_links = ('id', 'name','markaz', 'category','amount','date','recipient')


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('id','markaz', 'mentor','amount','status','type')
    list_display_links = ('id','markaz', 'mentor','amount','status','type')


