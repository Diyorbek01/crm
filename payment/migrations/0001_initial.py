# Generated by Django 3.2.7 on 2021-09-16 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0010_staff_date_joined'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('recipient', models.CharField(blank=True, max_length=150, null=True)),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('create_at', models.DateField(auto_now_add=True)),
                ('update_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('type', models.CharField(blank=True, choices=[('1', 'Naqd pul'), ('2', 'UZCARD'), ('3', 'Bank hisobi')], default=1, max_length=150, null=True)),
                ('create_at', models.DateField(auto_now_add=True)),
                ('update_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('1', 'Percent'), ('2', 'Cash')], max_length=150, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('1', 'Single'), ('2', 'Everybody')], max_length=150, null=True)),
                ('create_at', models.DateField(auto_now_add=True)),
                ('update_at', models.DateField(auto_now=True)),
                ('markaz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.markaz')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.staff')),
            ],
        ),
    ]