# Generated by Django 2.2.4 on 2019-08-30 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_pet_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
