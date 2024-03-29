# Generated by Django 2.2 on 2019-04-10 19:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('answer_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('answer', models.TextField(blank=True, max_length=255)),
                ('user_id', models.CharField(editable=False, max_length=300)),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.CharField(editable=False, max_length=300)),
                ('topics', models.CharField(choices=[('Mobility', 'Mobility'), ('Computer', 'Computer Hardware/Software'), ('Gamming', 'Gamming'), ('Security', 'Security'), ('Internet', 'Internet')], default='Mobility', max_length=50)),
                ('question', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True, max_length=255)),
                ('uploaded_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Fname', models.CharField(max_length=20)),
                ('Lname', models.CharField(max_length=20)),
                ('Address', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30)),
                ('Interest', multiselectfield.db.fields.MultiSelectField(choices=[('Mobility', 'Mobility'), ('Computer', 'Computer Hardware/Software'), ('Gamming', 'Gamming'), ('Security', 'Security'), ('Internet', 'Internet')], default='Computer', max_length=300, verbose_name='Select your interested topics')),
                ('profile', models.FileField(upload_to='documents/')),
                ('password', models.CharField(max_length=40)),
                ('status', models.CharField(default='NOT_VERIFIED', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(editable=False, max_length=300)),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Question')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.User')),
            ],
        ),
        migrations.CreateModel(
            name='Like_view',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type1', models.CharField(editable=False, max_length=300)),
                ('user_id', models.CharField(editable=False, max_length=300)),
                ('answer_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.Answer')),
                ('question_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.Question')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Question'),
        ),
    ]
