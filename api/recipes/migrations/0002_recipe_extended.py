# Generated by Django 3.2 on 2021-04-25 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='extended',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
