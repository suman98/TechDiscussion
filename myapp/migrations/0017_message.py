# Generated by Django 2.2 on 2019-04-15 12:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_delete_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_id', models.CharField(editable=False, max_length=300)),
                ('receiver_id', models.CharField(editable=False, max_length=300)),
                ('message', models.CharField(editable=False, max_length=300)),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
                ('is_read', models.BooleanField(default=False)),
            ],
        ),
    ]
