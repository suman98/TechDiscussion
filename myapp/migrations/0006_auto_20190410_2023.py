# Generated by Django 2.2 on 2019-04-10 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_auto_20190410_2020'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='image',
            new_name='question_img',
        ),
    ]