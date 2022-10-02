from group.models import *
from students.models import Students
from main.models import *


class Payment(models.Model):
    TYPE = (
        ('1', 'Naqd pul'),
        ('2', 'UZCARD/HUMO'),
        ('3', 'Bank hisobi'),
    )

    markaz = models.ForeignKey(Markaz, on_delete=models.CASCADE, null=True, blank=True)
    learner = models.ForeignKey(Students, on_delete=models.CASCADE, null=False, blank=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    month = models.IntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=150, choices=TYPE, default=1, null=True, blank=True)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.comment


class Category(models.Model):
    name = models.CharField(max_length=150, null=True, blank=True)
    markaz = models.ForeignKey(Markaz, on_delete=models.CASCADE, null=True, blank=True)
    typ = models.CharField(max_length=10, choices=(("Appear", "Appear"), ("Delete", "Delete")), default='Appear')


    def __str__(self) -> str:
        return self.name


class Expense(models.Model):
    markaz = models.ForeignKey(Markaz, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    recipient = models.CharField(max_length=150, null=True, blank=True)
    name = models.CharField(max_length=150, null=False, blank=False)
    typ = models.CharField(max_length=10, choices=(("Appear", "Appear"), ("Delete", "Delete")), default='Appear')
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class Salary(models.Model):
    TYPE = (
        ('1', 'Percent'),
        ('2', 'Cash'),
        ('3', 'Salary'),
    )
    STATUS = (
        ('1', 'Everybody'),
        ('2', 'Single'),
    )
    markaz = models.ForeignKey(Markaz, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=150, choices=TYPE, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=150, choices=STATUS, default=1, null=True, blank=True)
    typ = models.CharField(max_length=10, choices=(("Appear", "Appear"), ("Delete", "Delete")))
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

