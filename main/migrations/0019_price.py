# Generated by Django 3.2.7 on 2021-11-16 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_coursecategory_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.IntegerField(blank=True, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('discount', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
