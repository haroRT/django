# Generated by Django 3.2.25 on 2024-03-09 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('USER', 'User')], default='USER', max_length=5),
        ),
    ]