# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='YoutubeVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, null=True, blank=True)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('shared_at', models.DateTimeField()),
                ('post_id', models.CharField(max_length=255)),
                ('youtube_id', models.CharField(max_length=50, null=True, blank=True)),
                ('position', models.PositiveIntegerField(default=0)),
                ('thumbnail_url', models.CharField(max_length=255, null=True, blank=True)),
                ('profile', models.ForeignKey(related_name='videos', to='account.Profile')),
            ],
            options={
                'ordering': ['-shared_at'],
            },
        ),
    ]
