# Generated by Django 2.2 on 2019-04-10 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20190410_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_img',
            field=models.FileField(upload_to='question/'),
        ),
    ]
