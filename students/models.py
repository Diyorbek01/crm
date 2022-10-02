from django.db import models

from group.models import Group
from lead.models import Place
from main.models import *


class Students(models.Model):
    TYPE = (
        ('Appear', 'Appear'),
        ('Deleted', 'Deleted'),
    )
    Payment = (
        ('1', 'Paid'),
        ('2', 'Unpaid'),
    )
    name = models.CharField(max_length=150, null=True, blank=True)
    markaz = models.ForeignKey(Markaz, on_delete=models.CASCADE)
    lead_category = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True)
    phone = models.CharField(max_length=150, null=True, blank=True)
    birthday = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(("Erkak", "Erkak"), ("Ayol", "Ayol")), null=True, blank=True)
    photo = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    group = models.ManyToManyField(Group,default=1, null=True)
    comment = models.TextField(null=True, blank=True)
    parents_phone = models.CharField(max_length=150, null=True, blank=True)
    telegram = models.CharField(max_length=150, null=True, blank=True)
    address = models.CharField(max_length=150, null=True, blank=True)
    test = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=150, choices=TYPE, default='Appear', null=True, blank=True)
    payment_status = models.CharField(max_length=150, choices=Payment, default=2, null=True, blank=True)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name



class Attendance(models.Model):
    STATUS = (
        ('True', True),
        ('False', False),
    )

    markaz = models.ForeignKey(Markaz, on_delete=models.CASCADE)
    action = models.CharField(max_length=15, choices=STATUS, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

