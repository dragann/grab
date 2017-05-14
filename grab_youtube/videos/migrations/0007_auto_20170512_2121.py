# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_videorating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='youtubevideo',
            name='position',
        ),
        migrations.AddField(
            model_name='youtubevideo',
            name='hearts',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='youtubevideo',
            name='poos',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
