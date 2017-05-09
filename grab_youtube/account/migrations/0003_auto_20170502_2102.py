# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20170502_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='fb_user_id',
            field=models.CharField(default='a', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='friends',
            field=models.ManyToManyField(to='account.Profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='slug',
            field=models.CharField(default='a', max_length=255),
            preserve_default=False,
        ),
    ]
