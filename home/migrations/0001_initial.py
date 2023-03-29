# Generated by Django 4.1.7 on 2023-03-29 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='نام')),
                ('slug', models.SlugField(allow_unicode=True, max_length=200, unique=True, verbose_name='اسلاگ')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
                'ordering': ('-created', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='نام')),
                ('slug', models.SlugField(allow_unicode=True, max_length=200, unique=True, verbose_name='اسلاگ')),
                ('imag', models.ImageField(upload_to='products/media/imag', verbose_name='عکس')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('price', models.IntegerField(verbose_name='قیمت')),
                ('available', models.BooleanField(default=True, verbose_name='موجود')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='زمان بروزرسانی محصول')),
                ('category', models.ManyToManyField(related_name='products', to='home.category', verbose_name='دسته')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
                'ordering': ('-updated', '-created'),
            },
        ),
    ]
