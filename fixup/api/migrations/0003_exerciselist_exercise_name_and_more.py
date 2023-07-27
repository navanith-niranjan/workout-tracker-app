# Generated by Django 4.2.3 on 2023-07-27 21:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_age_user_height_user_sex_user_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciselist',
            name='exercise_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='exerciselist',
            name='exercise_type',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='sessions',
            name='distance',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='sessions',
            name='exercise',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.exerciselist'),
        ),
        migrations.AddField(
            model_name='sessions',
            name='kgorlb',
            field=models.CharField(max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='sessions',
            name='kmormiles',
            field=models.CharField(max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='sessions',
            name='notes',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='sessions',
            name='pace',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='sessions',
            name='reps',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='sessions',
            name='session_duration',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='sessions',
            name='sets',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='sessions',
            name='time',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='sessions',
            name='weight',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='sessions',
            name='workout_history',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.workouthistory'),
        ),
        migrations.AddField(
            model_name='workouthistory',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='workouthistory',
            name='session_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='workouthistory',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='height',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('N', 'Not Specified')], max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='weight',
            field=models.FloatField(null=True),
        ),
    ]
