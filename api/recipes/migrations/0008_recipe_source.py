# Generated by Django 3.2 on 2021-06-23 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_alter_trip_when'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='source',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
