# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=60)),
                ('userCount', models.IntegerField()),
                ('problemCount', models.IntegerField()),
                ('allAcCount', models.IntegerField()),
                ('orgId', models.IntegerField()),
                ('source', models.CharField(max_length=30)),
            ],
        ),
    ]
