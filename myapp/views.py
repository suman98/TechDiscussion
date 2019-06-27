from django.shortcuts import render,redirect
from django.http import HttpResponse
# # from django.core.mail import EmailMessage
import random
from .logical import Logic
from queryset_sequence import QuerySetSequence
from .intelligence import spelling_checker,Related_question,Navies
from .models import User,Question,Answer,Like_view,Report,Message
from .forms import UserForm,QuestionForm
import math

# Create your views here.i
def index(request):
	if request.method=="GET" and "page" in request.GET:
		page=int(request.GET.get('page'))
		y=page*15
		x=y-15
	else:
		x=0
		y=15
	# if request.method=="GET" and search in request.GET:
	if ("username" in request.session ):
		users=request.session['username']
		notify=(Logic().Notifications(request.session['username'],None))
		message=(Logic().Message(request.session['username'],"calc"))
		if request.method=="GET" and "select" in request.GET:
			q_posts=Logic().select_post(request.GET.get('select'),users)
		else:
			q_posts=[]
			for topic in (User.objects.get(user_id=users)).Interest:
				q_posts.extend(list(Question.objects.filter(topics__contains=topic).order_by('-uploaded_at'))[0:15])#finding the topics from multiselct field or loop over multiselect field
			random.shuffle(q_posts)
	else:
		users=None #ya users sanga matlab xain tesaile None
		notify=0
		message=0
		if request.method=="GET" and "select" in request.GET:
			q_posts=Logic().select_post(request.GET.get('select'),users)
		else:
			q_posts=Question.objects.all().order_by('-uploaded_at')
	q_post=q_posts[x:y]
	post=Logic().post(q_post,users) 
	t_page=math.ceil(len(q_posts)/15)
	return render(request,'home.html',{'Cmessage':message,'post_home':post,'notify':notify,'total_page':[i for i in range(1,t_page+1)]})

def logout(request):
	if "username" in request.session:
		del request.session['username']
	if "profile" in request.session:
		del request.session['profile']
	return redirect('index')

def check_login(request):
	if request.method=="POST" and "v_code" in request.POST:
		code=request.POST.get('v_code')
		u_id=request.POST.get('u_id')
		if code==request.session['code_for_validate']:
			user=User.objects.get(user_id=u_id)
			user.status="verified"
			user.save()
			del request.session['code_for_validate']
			return render(request,'base/login.html',{'alert':"ACCOUNT VERIFIED ENTER USERNAME AND PASSWORD TO CONTINUE"})
		else:
			return render(request,'base/login.html',{'alert':"Could not verify please try again"})
	if request.method=="POST" and "user_id" in request.POST:
		user_id=request.POST.get('user_id')
		password=request.POST.get('pass')
		checking=User.objects.filter(user_id=user_id,password=password) #iexact ignors small captial letter
		if checking.exists():
			# if (User.objects.get(user_id=user_id)).status=="verified":
			request.session['username']=user_id
			request.session['profile']=(User.objects.get(user_id=user_id)).profile.url
			# 	return redirect('index')
			return redirect('index')
			# else:
			# 	check=User.objects.get(user_id=user_id)
			# 	checking1=(User.objects.filter(status="verified",email=check.email))
			# 	if checking1.exists():
			# 		check.delete()
			# 		return render(request,'base/login.html',{'alert':"Sorry This account is removed Yours email has already been activate with another account "})
			# 	try:
			# 		code=str(randint(1000,9999))
			# 		validate = "Verification code is " + code
			# 		email = EmailMessage('Technical Disussion', validate, to=[check.email])
			# 		email.send()
			# 		request.session['code_for_validate']=str(code)
			# 		return render(request,'validate.html',{'id':user_id})
			# 	except Exception:
			# 		return render(request,'base/login.html',{'alert':"NO CONNECTIONS PLEASE CONNECT TO INTERNET TO ACTIVATE YOURS ACCOUNT"})
		else:
			return render(request,'base/login.html',{'alert':"Invalid Username or password"})
	return render(request,'base/login.html')

def signup(request):
  # return render(request,'popup.html',{'val1':"hahah"})
  form=UserForm(request.POST,request.FILES)
  if request.method=="POST" and "user_id" in request.POST:
    sid=request.POST.get('user_id')
    email=request.POST.get('email')
    id_check=User.objects.filter(user_id=sid)
    email_check=User.objects.filter(email=email,status="verified")
    if id_check.exists() or sid==None:
      return render(request,'base/signup.html',{'form':form,'id_check':"USER ID ALREADY TAKEN or Invalid"})
    if email_check.exists():
      return render(request,'base/signup.html',{'form':form,'email_check':"Email ALREADY TAKEN"})
  if form.is_valid():
    form.save()
    return render(request,'base/login.html',{'alert':"ACCOUNT CREATED "})
  else:
    form=UserForm()
  return render(request,'base/signup.html',{'form':form})


def ask(request):
	if "username" not in request.session:
		return HttpResponse("<h1>Hey you must login first</h1>")
	form=QuestionForm(request.POST,request.FILES,request.session)
	if request.method=="POST" and "description" in request.POST:
		if form.is_valid():
			form.instance.user_id=request.session['username']
			form.save()
			return redirect('profile')
		else:
			form=QuestionForm()
	elif request.method=="POST" and "question" in request.POST:
		try1=request.POST.get('try')
		question=request.POST.get('question')
		if try1=="second":
			check_duplicate=Related_question(question,Question.objects.all()).Recommend()
			if check_duplicate[0]=="error":
				return render(request,'questions.html',{'warning':"error"})
			if max(check_duplicate[1])>99: #checking dublicate Question
				return render(request,'questions.html',{'warning':check_duplicate[0][0]})
			topic=Navies(question).navies_bays()
			form=QuestionForm(initial={'topics':topic,'question':question})
			return render(request,'questions.html',{'form':form,'check2':question,'similar':check_duplicate[0][0:7],'topic':topic})
		if "on_spell" in request.POST:
			final_sentence=spelling_checker(question).spell()
			form=QuestionForm(initial={'question':final_sentence[0]})
		else:
			final_sentence=[question,question]
		if final_sentence[0].lower()==final_sentence[1].lower():
			check_duplicate=Related_question(final_sentence[0],Question.objects.all()).Recommend()
			if check_duplicate[0]=="error":
				return render(request,'questions.html',{'warning':"error"})
			if max(check_duplicate[1])>99: #checking dublicate Question
				return render(request,'questions.html',{'warning':check_duplicate[0][0]})
			topic=Navies(question).navies_bays()
			form=QuestionForm(initial={'topics':topic,'question':question})
			return render(request,'questions.html',{'form':form,'check2':final_sentence[0],'similar':check_duplicate[0][0:7],'topic':topic})
		else:
			return render(request,'questions.html',{'form':form,'check':"second",'corrected':final_sentence[0]})
	form=QuestionForm()
	return render(request,'questions.html',{'form':form,'check':"first"})

def post_ans(request):
	if request.method=="POST" and "answer" in request.POST and "username" in request.session:
		question_id=request.POST.get('question_id')
		answer=request.POST.get('answer')
		user_id=request.session['username']
		if 'answer_img' in request.FILES:
			answer_img=request.FILES['answer_img']
			answer_data1=Answer(question_id=(Question.objects.get(question_id=question_id)),user_id=user_id,answer=answer,answer_img=answer_img)
		else:
			answer_data1=Answer(question_id=(Question.objects.get(question_id=question_id)),user_id=user_id,answer=answer)
		answer_data1.save()

def view_item(request):
	try:
		question_id=request.GET.get('question_id')
		q_posts=[]
		for topic in Question.objects.get(question_id=question_id).topics: #system will only find the similar question based on topics
			q_posts.extend(list(Question.objects.filter(topics__contains=topic).exclude(question_id=question_id)))
		query=Logic().unique_post(q_posts) #since q_post might contain dublcate post due to topics so we need to extract the unique topic based on question_id
		related_qus=Related_question(Question.objects.get(question_id=question_id).question,query).Recommend()
		if "username" in request.session:
			welcome_check=Like_view.objects.filter(question_id=question_id,user_id=request.session['username'],type1="view")
			if welcome_check.exists()==False:
				welcome=Like_view(question_id=Question.objects.get(question_id=question_id),user_id=request.session['username'],type1="view")
				welcome.save()
		question=Question.objects.get(question_id=question_id)
		if "username" in request.session:
			users=request.session['username']
		else:
			users=None
		answer_data=Logic().answers(users,question_id)
		if related_qus[0]=="NOTHING" or related_qus[0]=="error" :
			related="NOTHING"
		else:
			related=zip((related_qus[0])[0:7],(related_qus[1])[0:7])
		return render(request,'show.html',{'Related':related,'Question':question,'Answer':answer_data[0],'total_ans':answer_data[1]})
	except:
		return HttpResponse("<h1>PAGE NOT FOUND</h1>")
def like_view(request):
	if "username" not in request.session:
		return HttpResponse("<h1>Hey you must login first</h1>")
	question_id=request.GET.get('question_id')
	if request.method=="GET" and "like_view" in request.GET:
		type1=request.GET.get('like_view')
		if type1=="anslike":
			name=(Answer.objects.get(answer_id=question_id).user_id)
			question_ref=Question.objects.get(question_id=((Answer.objects.get(answer_id=question_id)).question_id.question_id))
			check=Like_view.objects.filter(answer_id=question_id,user_id=request.session['username'],type1="like")
			if check.exists():
				like1=Like_view.objects.get(answer_id=question_id,user_id=request.session['username'],type1="like")
				like1.delete()
				like=[len(Like_view.objects.filter(answer_id=question_id,type1="like")),'no']
				return render(request,'base/ajax.html',{'anslike':like,'ans_id':question_id,'name':name,'Question_ref':question_ref})
			else:
				like1=Like_view(answer_id=Answer.objects.get(answer_id=question_id),user_id=request.session['username'],type1="like")
				like1.save()
				like=[len(Like_view.objects.filter(answer_id=question_id,type1="like")),'yes']
				return render(request,'base/ajax.html',{'anslike':like,'ans_id':question_id,'name':name,'Question_ref':question_ref})
		name=(Question.objects.get(question_id=question_id).user_id)
		if (type1=="like"):
			viewss_ans=[len(Like_view.objects.filter(question_id=question_id,type1="view")),len(Answer.objects.filter(question_id=question_id))]
			check=Like_view.objects.filter(question_id=question_id,user_id=request.session['username'],type1="like")
			if check.exists():
				like1=Like_view.objects.get(question_id=question_id,user_id=request.session['username'],type1="like")
				like1.delete()
				like=[len(Like_view.objects.filter(question_id=question_id,type1="like")),'no']
				return render(request,'base/ajax.html',{'like':like,'question_id':question_id,'name':name,'views':viewss_ans})
			else:
				like1=Like_view(question_id=Question.objects.get(question_id=question_id),user_id=request.session['username'],type1="like")
				like1.save()
				like=[len(Like_view.objects.filter(question_id=question_id,type1="like")),'yes']
				return render(request,'base/ajax.html',{'like':like,'question_id':question_id,'name':name,'views':viewss_ans})
		
def profile(request):
	try:
		if request.method=="GET" and 'answer_q' in request.GET:
			profile=request.GET.get('answer_q')
			type1=request.GET.get('type1')
			if type1=="answer":
				answer=(Answer.objects.filter(user_id=request.GET.get('answer_q')).only("question_id","user_id"))
				Question1=Question.objects.filter(question_id__in=[obj.question_id.question_id for obj in answer]).order_by('-uploaded_at')
				if len(Question1)==0:
					Question1=""
			else:
				like_view=(Like_view.objects.filter(user_id=profile,type1=type1)).exclude(question_id__isnull=True).order_by('-uploaded_at')
				Question1=(Question.objects.filter(question_id__in=[str(obj.question_id.question_id) for obj in like_view]))
			return render(request,'base/ajax.html',{'Question':Question1})
		if request.method=="GET" and "profile" in request.GET:
			profile=request.GET.get('profile')
		else:
			if "username" not in request.session:
				return HttpResponse("<h1>Hey you must login first</h1>")
			profile=request.session['username']
		q_post=Question.objects.filter(user_id=profile).order_by('-uploaded_at')
		if q_post.exists()==False:
			q_post=""
		user_given_ans=len((set([str(obj.question_id.question_id) for obj in (Answer.objects.filter(user_id=profile).only("question_id"))])))
		counting_data=[user_given_ans,len(Like_view.objects.filter(user_id=profile,type1="like").exclude(question_id__isnull=True)),len(Like_view.objects.filter(user_id=profile,type1="view"))]
		return render(request,'profile.html',{'user_profile':User.objects.get(user_id=profile),'Question':q_post,'user_data_q':counting_data})
	except:
		return HttpResponse("<h1>PAGE NOT FOUND</h1>")
def report(request):
	if "username" not in request.session:
		return HttpResponse("<h1>Hey you must login first</h1>")
	if request.method=="GET" and "report_msg" in request.GET:
		report_msg=request.GET.get('report_msg')
		question_id=request.GET.get('question_id')
		report=Report(user_id=User.objects.get(user_id=request.session['username']),question_id=Question.objects.get(question_id=question_id),message=report_msg)
		report.save()

def Notification(request):
	if "username" not in request.session:
		return HttpResponse("<h1>Hey you must login first</h1>")
	nofify=Logic().Notifications(request.session['username'],"show")
	notifications=[]
	for obj in nofify: #apa koko user lae like answer gare nikalne
		questions=Question.objects.get(question_id=(obj[1]).question_id.question_id)
		if obj[0]=="like":
			user_obj=(Like_view.objects.filter(question_id=(obj[1].question_id),type1="like").order_by('-uploaded_at')).exclude(user_id=request.session['username'])
			users=[]
			for obj in user_obj:
				if obj.user_id not in users:
					users.append(obj.user_id)
			notifications.append(["like",questions,users])
		elif obj[0]=="ans":
			user_obj=(Answer.objects.filter(question_id=(obj[1].question_id)).order_by('-uploaded_at')).exclude(user_id=request.session['username'])
			users=[]
			for obj in user_obj:
				if obj.user_id not in users:
					users.append(obj.user_id)
			notifications.append(["ans",questions,users])
	return render(request,'popup.html',{'notifications':notifications})

def search(request):
	if request.method=="GET" and "search_q" in request.GET:
		if request.method=="GET" and "no_correction" in request.GET:
			search_q=(request.GET.get('no_correction')).lower()
			try1="None"
		else:
			search_q=(request.GET.get('search_q')).lower()
			try1="None"
			if(len(search_q)<100): #dont correct the spelling if the sentence length is greater than 100
				corrected=spelling_checker(search_q).spell() 
				search_q=corrected[0]
				if search_q.lower()==corrected[1].lower():
					try1="None"
				else:
					try1=[search_q,corrected[1]]
		result=Related_question(search_q,Question.objects.all()).Recommend()
		if result[0]=="NOTHING":
			post=""
		elif result[0]=="error":  #yedi stop word ko karan le result aauna sakena vani
			result=Question.objects.filter(question__icontains=search_q)
			if result.exists():
				post=Logic().post(result,None)
			else:
				post="" 
		else:
			post=Logic().post(result[0],None) #ya users sanga matlab xain tesaile None and list ko 0 ma ans xa question ko objects ko
		return render(request,'home.html',{'post_home':post,'next':try1})
	else:
		return HttpResponse("ERROR")

def message(request):
	if "username" not in request.session:
		return HttpResponse("<h1>Hey you must login first</h1>")
	if request.method=="POST" and "message" in request.POST:
		sender=request.session['username']
		receiver=request.POST.get('receiver')
		message=request.POST.get('message')
		new=Message(sender_id=sender,receiver_id=receiver,message=message)
		new.save()
	if request.method=="GET" and "show_msg" in request.GET:
		notify=Logic().Message(request.session['username'],request.GET.get('show_msg'))
		return render(request,'popup.html',{'Message':notify})
	if request.method=="GET" and "receiver" in request.GET:
		receiver=request.GET.get('receiver')
	message=QuerySetSequence(Message.objects.filter(sender_id=request.session['username'],receiver_id=receiver),Message.objects.filter(sender_id=receiver,receiver_id=request.session['username'])).order_by('-uploaded_at')
	if message.exists()==False:
		message="Empty"
	return render(request,'messaging.html',{'Message':message,'receiver':User.objects.get(user_id=receiver)})

def delete(request):
	if "username" not in request.session:
		return HttpResponse("<h1>Hey you must login first</h1>")
	if request.method=="GET" and 'question_id' in request.GET:
		pid=request.GET.get('question_id')
		pobj=Question.objects.get(question_id=pid)
		if pobj.user_id==request.session['username']:
			pobj.delete()
	if request.method=="GET" and 'answer_id' in request.GET:
		pid=request.GET.get('answer_id')
		pobj=Answer.objects.get(answer_id=pid)
		if pobj.user_id==request.session['username'] or (pobj.question_id).user_id==request.session['username']:
			pobj.delete()

def ans_sort(request):
	if request.method=="GET" and "question_id" in request.GET:
		question_id=request.GET.get('question_id')
		ans_data=Answer.objects.filter(question_id=question_id)
		data1=[[obj,len(Like_view.objects.filter(answer_id=obj.answer_id))] for obj in ans_data ]
		view_like=sorted(data1, key=lambda x: x[1],reverse=True)[0:15]
		# x=[i[0] for i in view_like]
		data=Logic().sort_answer_data(view_like,request.session['username'])
		return render(request,'base/ajax.html',{'sort_ans':data})
	if request.method=="GET" and "ans_latest" in request.GET:
		question_id=request.GET.get('ans_latest')
		answer_data=Logic().answers(request.session['username'],question_id)
		return render(request,'base/ajax.html',{'sort_ans':answer_data[0]})