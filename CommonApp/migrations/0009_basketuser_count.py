# Generated by Django 5.0.4 on 2024-04-06 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CommonApp', '0008_basketuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='basketuser',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
