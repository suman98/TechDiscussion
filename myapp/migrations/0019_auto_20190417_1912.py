# Generated by Django 2.2 on 2019-04-17 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_auto_20190417_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_img',
            field=models.ImageField(blank=True, null=True, upload_to='question/'),
        ),
    ]
