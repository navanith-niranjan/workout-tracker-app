# Generated by Django 4.2.3 on 2023-07-28 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_customexerciselist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customexerciselist',
            name='exercises',
            field=models.ManyToManyField(to='api.exerciselist'),
        ),
    ]