# Generated by Django 3.0.3 on 2020-04-27 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amazonapp', '0006_auto_20200427_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, default='images/logo.jpg', null=True, upload_to=''),
        ),
    ]
