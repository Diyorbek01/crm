import os

from django.db import models


# choices
def upload_to(instance, filename):
    return f'posts/{filename}'.format(filename=filename)


STAFF_ROLE = (
    ('CEO', 'CEO'),
    ('Administrator', 'Administrator'),
    ('Teacher', 'Teacher'),
    ('Marketer', 'Marketer'),
    ('Cashier', 'Cashier'),
    ('Owner', 'Owner')
)


# markaz
class Markaz(models.Model):
    name = models.CharField(max_length=50)
    subdomain = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='profile_pics', blank=True, default='profile_pics/rootlogo.jpg')
    registered_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    def delete(self, *args, **kwargs):
        items = Markaz.objects.all()
        items.delete()

        try:
            os.remove(self.photo.name)
            super(Markaz, self).delete(*args, **kwargs)
        except FileNotFoundError:
            pass

    class Meta:
        verbose_name_plural = "Markazlar"


class Price(models.Model):
    period = models.CharField(max_length=80, null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.period

    class Meta:
        verbose_name_plural = "Narx"


class Staff(models.Model):
    TYPE = (
        ('Appear', 'Appear'),
        ('Delete', 'Delete'),
    )
    phone = models.CharField(max_length=17, unique=True)
    full_name = models.CharField(max_length=50)
    role = models.CharField(max_length=50, choices=STAFF_ROLE, null=True, blank=True)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(("Erkak", "Erkak"), ("Ayol", "Ayol")), null=True, blank=True)
    photo = models.ImageField(upload_to=upload_to, null=True, blank=True, default='profile_pics/rootlogo.jpg')
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    typ = models.CharField(max_length=150, choices=TYPE, default="Appear", null=False, blank=False)
    markaz = models.ForeignKey(Markaz, on_delete=models.CASCADE, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.full_name


# course
class Course(models.Model):
    markaz = models.ForeignKey(Markaz, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    typ = models.CharField(max_length=10, choices=(("Appear", "Appear"), ("Delete", "Delete")), default='Appear')
    price = models.IntegerField()
    duration = models.FloatField()
    description = models.TextField()
    photo = models.ImageField(upload_to='profile_pics', null=True, blank=True)

    def __str__(self) -> str:
        return self.name


# category for course details
class CourseCategory(models.Model):
    markaz = models.ForeignKey(Markaz, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.name


# extra details for course
class CoursePlan(models.Model):
    markaz = models.ForeignKey(Markaz, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, null=True)

    title = models.TextField(null=True, blank=True)
    duration = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title


# after graduate course
class CourseGraduate(models.Model):
    markaz = models.ForeignKey(Markaz, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    title = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title


# room
class Room(models.Model):
    markaz = models.ForeignKey(Markaz, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    typ = models.CharField(max_length=10, choices=(("Appear", "Appear"), ("Delete", "Delete")), default='Appear')


# history
class History(models.Model):
    markaz = models.ForeignKey(Markaz, on_delete=models.CASCADE)
    user = models.CharField(max_length=50)
    did = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)


class Bot(models.Model):
    markaz = models.ForeignKey(Markaz, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.markaz.name + "_bot"


class Chat(models.Model):
    markaz = models.ForeignKey(Markaz, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    user_chat_id = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.title


class Message(models.Model):
    text = models.TextField()
    own = models.BooleanField(default=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        super(Message, self).save(*args, **kwargs)
