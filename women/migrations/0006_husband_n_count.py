# Generated by Django 5.1.1 on 2024-09-13 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0005_husband_women_husband'),
    ]

    operations = [
        migrations.AddField(
            model_name='husband',
            name='n_count',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
