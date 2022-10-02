from django.db import models

from main.models import *


class Week(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)

    def __str__(self) -> str:
        return self.name


class Group(models.Model):
    STATUS = (
        ('Toq kunlari', 'Toq kunlari'),
        ('Juft kunlar', 'Juft kunlar'),
        ('Dam olish kuni', 'Dam olish kuni'),
        ('Har kuni', 'Har kuni'),
        ('Boshqa', 'Boshqa'),
    )

    TYPE = (
        ('Yangi', 'Yangi'),
        ('Jarayonda', 'Jarayonda'),
        ('Ochirilgan', 'Ochirilgan'),
    )
    markaz = models.ForeignKey(Markaz, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150, null=False, blank=False)
    student = models.IntegerField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    teacher = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True)
    days = models.CharField(max_length=150, choices=STATUS, null=False, blank=False)
    week = models.ManyToManyField(Week, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    start_lesson_at = models.TimeField(max_length=150, null=False, blank=False)
    start_group_at = models.DateField(null=False, blank=False)
    finish_group_at = models.DateField(null=False, blank=False)
    typ = models.CharField(max_length=150, choices=TYPE, default="Yangi", null=False, blank=False)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name
