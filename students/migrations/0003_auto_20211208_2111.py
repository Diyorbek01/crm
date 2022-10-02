# Generated by Django 3.2.7 on 2021-12-08 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0002_auto_20211122_1844'),
        ('students', '0002_auto_20211122_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='action',
            field=models.CharField(blank=True, choices=[('True', True), ('False', False)], max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='students',
            name='group',
            field=models.ManyToManyField(default=1, null=True, to='group.Group'),
        ),
        migrations.AlterField(
            model_name='students',
            name='type',
            field=models.CharField(blank=True, choices=[('Appear', 'Appear'), ('Deleted', 'Deleted')], default='Appear', max_length=150, null=True),
        ),
    ]
