# Generated by Django 4.0.4 on 2022-08-26 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_drivers_driver_about_me_drivers_driver_area_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentee',
            name='rentee_balance',
        ),
        migrations.RemoveField(
            model_name='spotowner',
            name='balance',
        ),
        migrations.AddField(
            model_name='users',
            name='user_balance',
            field=models.IntegerField(default=0, null=True, verbose_name='user_balance'),
        ),
    ]