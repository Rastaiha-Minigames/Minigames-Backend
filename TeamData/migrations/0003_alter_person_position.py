# Generated by Django 3.2.6 on 2021-08-17 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamData', '0002_auto_20210817_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='position',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]