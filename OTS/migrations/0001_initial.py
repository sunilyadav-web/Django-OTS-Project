# Generated by Django 3.2.9 on 2022-02-14 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Quetions',
            fields=[
                ('qeno', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('que', models.CharField(max_length=400)),
                ('optiona', models.CharField(max_length=100)),
                ('optionb', models.CharField(max_length=100)),
                ('optionc', models.CharField(max_length=100)),
                ('optiond', models.CharField(max_length=100)),
                ('answer', models.CharField(max_length=1)),
            ],
        ),
    ]
