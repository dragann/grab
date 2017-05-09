# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_auto_20170502_1802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youtubevideo',
            name='shared_by_fb_id',
        ),
        migrations.RemoveField(
            model_name='youtubevideo',
            name='shared_by_fb_name',
        ),
    ]
