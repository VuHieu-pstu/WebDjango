# Generated by Django 5.1.1 on 2024-09-19 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0008_alter_women_is_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='women',
            name='is_published',
            field=models.BooleanField(choices=[(0, 'черновик'), (1, 'Опубликовано')], default=1),
        ),
    ]
