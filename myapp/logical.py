from .models import User,Question,Like_view,Answer,Message
from queryset_sequence import QuerySetSequence
class Logic:	
	def like_calc(self,user,question_id,type2):
		if type2=="question":
			like_check=Like_view.objects.filter(question_id=question_id,type1="like")
			if like_check.exists():
				likes=len(like_check)
				if user is not None:
					if(Like_view.objects.filter(question_id=question_id,type1="like",user_id=user)).exists():
						user_like='yes'
					else:
						user_like='no'
				else:
					user_like="no"
				return ([likes,user_like])
			else:
				return ([0,'no'])
		if type2=="answer":
			like_check=Like_view.objects.filter(answer_id=question_id,type1="like")
			if like_check.exists():
				likes=len(like_check)
				if user is not None:
					if(Like_view.objects.filter(answer_id=question_id,type1="like",user_id=user)).exists():
						user_like='yes'
					else:
						user_like='no'
				else:
					user_like="no"
				return ([likes,user_like])
			else:
				return ([0,'no'])
				
	def select_post(self,select,user):
		if select=="interest":
			return Question.objects.filter(topics__in=(User.objects.get(user_id=user)).Interest).order_by('-uploaded_at')
		elif select=="view" or select=="like":
			views1=[]
			for obj in Question.objects.all():
				views1.append([len(Like_view.objects.filter(question_id=obj.question_id,type1=select)),obj.question_id])
			view_like=sorted(views1, key=lambda x: x[0],reverse=True)[0:15]
			views_like=[]
			for i in range(len(view_like)):
				views_like.append(Question.objects.get(question_id=view_like[i][1]))
			return views_like
		elif select=="latest":
			return Question.objects.all().order_by('-uploaded_at')
		else:
			return Question.objects.filter(topics__contains=select).order_by('-uploaded_at')
	def Notifications(self,user,show):
		try:
			question=Question.objects.filter(user_id=user)
			ans=Answer.objects.filter(question_id__in=[str(obj.question_id) for obj in question],is_read=False).exclude(user_id=user)
			likes=Like_view.objects.filter(question_id__in=[str(obj.question_id) for obj in question],type1="like",is_read=False).exclude(user_id=user)
			
			def find(ans,likes):
				notify=[]
				like_q=[]
				ans_q=[]
				objects= QuerySetSequence(ans,likes).order_by('-uploaded_at')
				for obj in objects:
					if hasattr(obj,'type1'): #type1 xa vani tyo like ma parxa
						if obj.question_id not in like_q:
							like_q.append(obj.question_id)
							notify.append(["like",obj])
					else:
						if obj.question_id not in ans_q:
							ans_q.append(obj.question_id)
							notify.append(["ans",obj])
				return notify

			if show=="show":
				if ans.exists():
					ans.update(is_read=True)
				if likes.exists():
					likes.update(is_read=True)
				ans=Answer.objects.filter(question_id__in=[str(obj.question_id) for obj in question]).exclude(user_id=user)
				likes=Like_view.objects.filter(question_id__in=[str(obj.question_id) for obj in question],type1="like").exclude(user_id=user)
				return (find(ans,likes))
				# if Answer.objects.filter(question_id=obj.question_id).exclude(user_id=user).exists():
				# 	if obj.question_id not in notify_q:
				# 		notify_q.append(obj.question_id)
				# if Like_view.objects.filter(question_id=obj.question_id,type1="like").exclude(user_id=user).exists():
				# 	if obj.question_id not in notify_L:
				# 		notify_L.append(obj.question_id)
			else:
				return len(find(ans,likes))
		except:
			return 0
	def answers(self,user,question_id):
		answer=Answer.objects.filter(question_id=question_id).order_by('-uploaded_at')
		profile=[]
		name=[]
		like=[]
		for obj in answer:
			profile.append((User.objects.get(user_id=obj.user_id)).profile)
			name.append((User.objects.get(user_id=obj.user_id)).Fname+" "+(User.objects.get(user_id=obj.user_id)).Lname)
			#mathi user ni check garnu parxa session ma xa ki nai vanera tesaile none
			like1=self.like_calc(user,obj.answer_id,"answer")
			like.append(like1)
		answer_data=zip(profile,name,answer,like)
		return [answer_data,len(name)]

	def post(self,q_post,user):
		profile=[]
		name=[]
		like=[]
		viewss_ans=[]
		dublicate=[]
		post=[]
		for obj in q_post:
			if obj.question_id not in dublicate:
				profile.append((User.objects.get(user_id=obj.user_id)).profile)
				fname=(User.objects.get(user_id=obj.user_id)).Fname
				lname=(User.objects.get(user_id=obj.user_id)).Lname
				name.append(fname+" "+lname)
				viewss_ans.append([len(Like_view.objects.filter(question_id=obj.question_id,type1="view")),len(Answer.objects.filter(question_id=obj.question_id))])
				like1=self.like_calc(user,obj.question_id,"question")
				like.append(like1)
				dublicate.append(obj.question_id)
				post.append(obj)
		post=zip(profile,name,post,like,viewss_ans)
		return post
	def unique_post(self,q_post):
		dublicate=[]
		post=[]
		for obj in q_post:
			if obj.question_id not in dublicate:
				dublicate.append(obj.question_id)
				post.append(obj)
		return post
	def Message(self,user,op):
		def unique(my_msg):
			notify_msg=[]
			msg=[]
			sender=[]
			for obj in my_msg:
				if obj.sender_id not in notify_msg:
					notify_msg.append(obj.sender_id)
					sender.append(User.objects.get(user_id=obj.sender_id))
					msg.append(obj)
			return [msg,sender]
		def unique_sent(my_msg):
			notify_msg=[]
			msg=[]
			receiver=[]
			for obj in my_msg:
				if obj.receiver_id not in notify_msg:
					notify_msg.append(obj.receiver_id)
					receiver.append(User.objects.get(user_id=obj.receiver_id))
					msg.append(obj)
			return [msg,receiver]

		if op=="calc":
			my_msg=Message.objects.filter(receiver_id=user,is_read=False)
			return (len(unique(my_msg)[0]))

		elif op=="received":
			my_msg=(Message.objects.filter(receiver_id=user)).order_by('-uploaded_at')
			if my_msg.exists():
				my_msg.update(is_read=True)
			msg=unique(my_msg)
			return zip(msg[0],msg[1])
		elif op=="sent":
			my_msg=(Message.objects.filter(sender_id=user)).order_by('-uploaded_at')
			msg=unique_sent(my_msg)
			return zip(msg[0],msg[1])
	def sort_answer_data(self,ans,user):
		profile=[]
		name=[]
		like=[]
		answer=[]
		for obj in ans:
			answer.append(obj[0])
			profile.append((User.objects.get(user_id=obj[0].user_id)).profile)
			name.append((User.objects.get(user_id=obj[0].user_id)).Fname+" "+(User.objects.get(user_id=obj[0].user_id)).Lname)
			#mathi user ni check garnu parxa session ma xa ki nai vanera tesaile none
			like1=self.like_calc(user,obj[0].answer_id,"answer")
			like.append(like1)
		answer_data=zip(profile,name,answer,like)
		return answer_data



