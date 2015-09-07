# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='review',
            field=models.ForeignKey(related_name='answers', blank=True, to='main.Review'),
        ),
    ]
