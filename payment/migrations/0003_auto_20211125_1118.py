# Generated by Django 3.2.7 on 2021-11-25 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20211122_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='typ',
            field=models.CharField(choices=[('Appear', 'Appear'), ('Delete', 'Delete')], default='Appear', max_length=10),
        ),
        migrations.AlterField(
            model_name='expense',
            name='typ',
            field=models.CharField(choices=[('Appear', 'Appear'), ('Delete', 'Delete')], default='Appear', max_length=10),
        ),
    ]
