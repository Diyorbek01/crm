# Generated by Django 3.2.7 on 2021-10-25 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_coursegraduate'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('markaz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.markaz')),
            ],
        ),
        migrations.CreateModel(
            name='CoursePlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.coursecategory')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.course')),
                ('markaz', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.markaz')),
            ],
        ),
    ]
