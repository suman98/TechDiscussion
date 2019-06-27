from django.utils import timezone
from multiselectfield import MultiSelectField
import uuid
from django.utils import timezone
from django.db import models

topics=(('Smartphone','Smartphone'),('Hardware','Hardware'),('Gamming','Gamming'),
		('Security','Security'),('Internet','Internet'),('Software and App','Software and App'))
# Create your models here.

class User(models.Model):
	user_id=models.CharField(max_length=20,primary_key=True)
	Fname=models.CharField(max_length=20,blank=False)
	Lname=models.CharField(max_length=20,blank=False)
	Address=models.CharField(max_length=20,blank=False)
	email=models.CharField(max_length=30,blank=False)
	Interest=MultiSelectField(choices=topics,max_length=300,blank=False,verbose_name="Select your interested topics")
	profile=models.ImageField(upload_to='documents/')
	password=models.CharField(max_length=40,blank=False)
	status = models.CharField(max_length=300,blank=False,default="NOT_VERIFIED")

class Question(models.Model):
	question_id=models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
	user_id=models.CharField(max_length=300,blank=False,editable=False)
	topics=MultiSelectField(choices=topics,max_length=300,blank=False,verbose_name="Select your interested topics")
	question=models.CharField(max_length=300,blank=False,unique=True)
	description=models.TextField(max_length=255,blank=True)
	question_img=models.ImageField(upload_to='question/',null=True,blank=True)
	uploaded_at = models.DateTimeField('date created', default=timezone.now)
	

class Answer(models.Model):
	answer_id=models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
	question_id=models.ForeignKey(Question,on_delete=models.CASCADE)
	answer=models.TextField(max_length=255,blank=False)
	user_id=models.CharField(max_length=300,blank=False,editable=False)
	answer_img=models.ImageField(upload_to='answer/',null=True,blank=True)
	is_read=models.BooleanField(default=False)
	uploaded_at = models.DateTimeField('date created', default=timezone.now)

class Like_view(models.Model):
	type1=models.CharField(max_length=300,blank=False,editable=False)
	question_id=models.ForeignKey(Question,on_delete=models.CASCADE,blank=True,null=True)
	answer_id=models.ForeignKey(Answer,on_delete=models.CASCADE,blank=True,null=True)
	user_id=models.CharField(max_length=300,blank=False,editable=False)
	uploaded_at = models.DateTimeField('date created', default=timezone.now)
	is_read=models.BooleanField(default=False)

class Report(models.Model):
	user_id=models.ForeignKey(User,on_delete=models.CASCADE,blank=False)
	question_id=models.ForeignKey(Question,on_delete=models.CASCADE,blank=False)
	message=models.CharField(max_length=300,blank=False,editable=False)

class Message(models.Model):
	sender_id=models.CharField(max_length=300,blank=False,editable=False)
	receiver_id=models.CharField(max_length=300,blank=False,editable=False)
	message=models.CharField(max_length=300,blank=False,editable=False)
	uploaded_at = models.DateTimeField('date created', default=timezone.now)
	is_read=models.BooleanField(default=False)

