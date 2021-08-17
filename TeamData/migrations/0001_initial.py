# Generated by Django 3.2.6 on 2021-08-16 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('Description', models.TextField()),
                ('Team', models.CharField(choices=[('کمیته برگزاری', 'Komite'), ('فنی', 'Fani'), ('برندینگ', 'Branding'), ('علمی', 'Elmi'), ('رسانه', 'Resaneh'), ('مسابقه', 'Mosabeghe')], default='کمیته برگزاری', max_length=50)),
                ('Picture', models.ImageField(upload_to='TeamImages/')),
            ],
        ),
    ]