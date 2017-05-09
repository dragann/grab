# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_auto_20170504_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubevideo',
            name='archived_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='youtubevideo',
            name='shared_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
