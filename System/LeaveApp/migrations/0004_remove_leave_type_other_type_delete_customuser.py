# Generated by Django 5.0.2 on 2024-03-01 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LeaveApp', '0003_customuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leave_type',
            name='other_type',
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
