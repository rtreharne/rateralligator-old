# Generated by Django 4.1.5 on 2023-01-06 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gator', '0002_comment_agree_comment_disagree'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='abuse',
            field=models.IntegerField(default=0),
        ),
    ]
