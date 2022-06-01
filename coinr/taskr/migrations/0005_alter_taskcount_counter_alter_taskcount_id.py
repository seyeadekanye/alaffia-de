# Generated by Django 4.0.4 on 2022-06-01 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskr', '0004_taskcount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskcount',
            name='counter',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='taskcount',
            name='id',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
