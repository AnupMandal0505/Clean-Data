# Generated by Django 5.0.2 on 2024-03-07 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_user_new_csv_alter_user_old_csv'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='new_csv',
        ),
        migrations.RemoveField(
            model_name='user',
            name='old_csv',
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='None', max_length=255),
        ),
    ]
