# Generated by Django 3.2.7 on 2021-11-25 05:56

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_room_typ'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=main.models.upload_to),
        ),
    ]