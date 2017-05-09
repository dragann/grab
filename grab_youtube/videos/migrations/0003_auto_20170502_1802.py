# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_youtubevideo_privacy'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubevideo',
            name='shared_by_fb_id',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='youtubevideo',
            name='shared_by_fb_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
