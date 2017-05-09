# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubevideo',
            name='privacy',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
