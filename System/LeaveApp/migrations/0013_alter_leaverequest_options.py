# Generated by Django 5.0.2 on 2024-03-25 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LeaveApp', '0012_alter_employee_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='leaverequest',
            options={'permissions': [('can_see_approved_leave', 'can see approved leave'), ('can_see_submitted_leave', 'can see submitted leave')]},
        ),
    ]