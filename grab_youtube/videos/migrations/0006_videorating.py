# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_profile_gender'),
        ('videos', '0005_auto_20170505_1743'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('rating', models.CharField(blank=True, max_length=50, null=True, choices=[(b'heart', b'Fucking A!'), (b'poo', b"It's crap")])),
                ('profile', models.ForeignKey(related_name='video_ratings', to='account.Profile')),
                ('video', models.ForeignKey(related_name='ratings', to='videos.YoutubeVideo')),
            ],
        ),
    ]
