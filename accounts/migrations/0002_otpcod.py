# Generated by Django 4.1.7 on 2023-03-27 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtpCod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=11, verbose_name='شماره تماس')),
                ('code', models.PositiveSmallIntegerField(max_length=4, verbose_name='کد تایید')),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]