# Generated by Django 2.2 on 2019-04-13 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_auto_20190411_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(editable=False, max_length=300)),
                ('temp_nofi', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='question',
            name='question_img',
            field=models.FileField(blank=True, null=True, upload_to='question/'),
        ),
    ]