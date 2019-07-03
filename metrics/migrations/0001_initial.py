# Generated by Django 2.2.3 on 2019-07-03 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Metrics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('channel', models.CharField(max_length=128)),
                ('country', models.CharField(max_length=16)),
                ('os', models.CharField(max_length=32)),
                ('impressions', models.IntegerField()),
                ('clicks', models.PositiveIntegerField()),
                ('installs', models.PositiveIntegerField()),
                ('spend', models.FloatField()),
                ('revenue', models.FloatField()),
            ],
        ),
    ]
