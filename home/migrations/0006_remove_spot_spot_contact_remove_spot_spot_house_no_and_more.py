# Generated by Django 4.0.4 on 2022-08-24 04:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_spot_spot_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='spot',
            name='spot_contact',
        ),
        migrations.RemoveField(
            model_name='spot',
            name='spot_house_no',
        ),
        migrations.RemoveField(
            model_name='spot',
            name='spot_name',
        ),
        migrations.RemoveField(
            model_name='spot',
            name='spot_road_no',
        ),
        migrations.AddField(
            model_name='spot',
            name='spot_house',
            field=models.CharField(default=django.utils.timezone.now, max_length=200, verbose_name='spot_house'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='spot',
            name='spot_number',
            field=models.CharField(max_length=200, null=True, verbose_name='spot_number'),
        ),
        migrations.AddField(
            model_name='spot',
            name='spot_road',
            field=models.CharField(default=django.utils.timezone.now, max_length=200, verbose_name='spot_road'),
            preserve_default=False,
        ),
    ]