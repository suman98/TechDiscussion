# Generated by Django 2.2 on 2019-04-10 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20190410_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='image',
            field=models.FileField(upload_to='documents/'),
        ),
    ]
