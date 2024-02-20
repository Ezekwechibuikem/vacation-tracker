# Generated by Django 5.0.2 on 2024-02-18 13:26

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('department', models.CharField(max_length=50)),
                ('unit', models.CharField(max_length=50)),
                ('role_id', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(6)])),
            ],
        ),
        migrations.CreateModel(
            name='leave',
            fields=[
                ('leave_id', models.AutoField(primary_key=True, serialize=False)),
                ('type_name', models.CharField(blank=True, max_length=50, null=True)),
                ('other_leave', models.CharField(blank=True, max_length=100, null=True)),
                ('comments', models.CharField(blank=True, max_length=250, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('date_applied', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('resumption_date', models.DateField(blank=True, null=True)),
                ('entitlement', models.IntegerField(blank=True, default=20, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(30)])),
                ('days_taken', models.IntegerField(blank=True, default=0)),
                ('remaining_days', models.IntegerField(blank=True, default=0)),
                ('approved', models.BooleanField(default=False, verbose_name='Approved')),
                ('emp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LeaveApp.employee')),
            ],
        ),
    ]
