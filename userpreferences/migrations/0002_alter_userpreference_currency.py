# Generated by Django 5.0.2 on 2024-03-15 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpreferences', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpreference',
            name='currency',
            field=models.CharField(default='No Currency', max_length=225, verbose_name='Currency'),
        ),
    ]
