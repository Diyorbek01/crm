from django.db import models
from main.models import Course, Markaz


# Create your models here.


class Place(models.Model):
    name = models.CharField(max_length=100)
    markaz = models.ForeignKey(Markaz, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Lead(models.Model):
    TYPE = (
        ('Yangi', 'Yangi'),
        ('Aloqada', 'Aloqada'),
        ('Delete', 'Delete'),
    )
    markaz = models.ForeignKey(Markaz, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=17)
    description = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    where = models.ForeignKey(Place, on_delete=models.CASCADE)
    status = models.CharField(max_length=150, choices=TYPE, default="Yangi", null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.full_name
