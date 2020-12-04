# Generated by Django 3.1.4 on 2020-12-04 10:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem_id', models.CharField(max_length=32)),
                ('title', models.CharField(max_length=128)),
                ('link', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('sdut', 'sdut'), ('poj', 'poj')], max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='SourceUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=128)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='source.source')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(choices=[('ac', 'Accepted'), ('wa', 'WrongAnswer')], max_length=32)),
                ('language', models.CharField(choices=[('c', 'C'), ('cpp', 'CPP'), ('py', 'Python')], max_length=32)),
                ('time_used', models.IntegerField()),
                ('memory_used', models.IntegerField()),
                ('length', models.IntegerField()),
                ('run_id', models.CharField(max_length=32)),
                ('submitted_at', models.DateTimeField()),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='source.problem')),
                ('source_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='source.sourceuser')),
            ],
        ),
        migrations.AddField(
            model_name='problem',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='source.source'),
        ),
    ]
