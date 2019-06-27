import os
import numpy
import math
import pandas as pd
from scipy import spatial
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import inflect #singular
p = inflect.engine()
ps = PorterStemmer()

#Spell checker Start here
class spelling_checker:
	def __init__(self,word_input):
		self.dic_word = numpy.array(pd.read_csv(open(os.getcwd()+"/myapp/training/dictionary.csv")))
		self.stem_word = numpy.array(pd.read_csv(open(os.getcwd()+"/myapp/training/dict.csv")))
		self.word_input=word_input
	def edit_distance(self,x):
		try:
			int(x)
			return x
		except Exception:
			if x.lower() in self.dic_word or ps.stem(x.lower()) in self.stem_word or p.singular_noun(x.lower()) in self.dic_word or p.plural(x.lower()) in self.dic_word or len(x)==1:
				return x
		if x.isupper()==True:
			return x
		if((x[0] and x[len(x)-1])=='"' or (x[0] and x[len(x)-1]=="'")):
			return x
		y=0
		for i in x:
			if i.isalpha():
				y=1
				break
		if y==0:
			return x
		str1="#"+x.lower()
		result=[]
		for  i in self.dic_word:
			temp=str(i[0])
			str2="@"+temp.lower()
			matrix=numpy.zeros((len(str2),len(str1)))#zero number rakera matrix banauxa
			for i in range(len(str1)):
				matrix[0][i]=i
			for j in range(len(str2)):
				matrix[j][0]=j
			for i in range(1,len(str2)):
				for j in range(1,len(str1)):
					# print(str1[j],str2[i])
					if(str1[j]==str2[i]):
						matrix[i][j]=matrix[i-1][j-1]
					else:
						matrix[i][j]=(1+min(matrix[i][j-1],matrix[i-1][j],matrix[i-1][j-1]))
			distance=[matrix[len(temp)][len(x)],temp]
			if distance[0]==1:
				return temp
			result.append(distance)
			# print(matrix)
		edit_distance_value=min(result, key=lambda x: x[0])
		# print(edit_distance_value[1])
		return edit_distance_value[1]

	def spell(self):
		word_N=(self.word_input).split()
		print(word_N)
		corrected=[]
		for i in word_N:
			edit_distances=self.edit_distance(i)
			corrected.append(edit_distances)
		result=(' '.join(corrected))
		chek=(' '.join(word_N))
		return [result,chek]

# TF_IDF starts here
class Related_question:
	def __init__(self,input_sen,all_d):
		data1 = pd.read_csv(open(os.getcwd()+"/myapp/training/stop.csv"))
		stop_word= data1["stop"].to_list()
		all_document=[]
		ques=(input_sen.lower()).split()
		doc_inp=[ps.stem(obj) for obj in ques if obj not in stop_word and len(obj)>1]#removing stop word from given sentences
		all_document.append(doc_inp)
		actual=[input_sen] #actual sentene to show final resul # print(actual)
		for obj in all_d:
			questions=((obj.question).lower()).split()
			sentence=[]
			sentence=[ps.stem(obj) for obj in questions if obj not in stop_word and len(obj)>1] #removing stop words from all documents
			if len(sentence)>0:
				actual.append(obj) # actual document to show as result
				all_document.append(sentence)
		self.actual_doc=actual
		self.all_doc=all_document
		# print(self.all_doc)
		
	def tokenize(self):
		unique_words=[]
		for sentence in self.all_doc:
			for word in sentence:
				if word not in unique_words:
					unique_words.append(word)
		return unique_words

	def IDF(self,unique_words):
		t_doc=len(self.all_doc)
		idf=[]
		for word in unique_words:
			word_all_doc=0
			for sentence in self.all_doc:
				if word in sentence:
					word_all_doc+=1
			# print(word,t_doc,word_all_doc)
			idf_c=math.log10(t_doc/word_all_doc)+1
			idf.append(idf_c)
		# print(idf)
		return idf

	def TF(self,unique_words):
		T_F=[]
		for sentence in self.all_doc:
			sen_len=len(sentence) 
			T_F_sen=[]
			for word in unique_words:
				word_len=sentence.count(word)
				# print(sentence,word,word_len,sen_len)
				T_F_sen.append(float(word_len/sen_len))
			T_F.append(T_F_sen)
		# print(T_F)
		return T_F

	def TF_IDF(self,TF,IDF):
		TF_IDF_doc=[]
		for sentence_TF in TF :
			TF_IDF_sen=[]
			data=zip(sentence_TF,IDF)
			for x,y in data:
				z=float(x*y)
				TF_IDF_sen.append(z)
			TF_IDF_doc.append(TF_IDF_sen)
		return TF_IDF_doc

	def cosine_sim(self,data):
		# cosine_similarity=[]
		# comp_data=data[0] #yo chai vector of given document or select gareko document 
		# def mag(mdata):
		# 	mag=0
		# 	for i in mdata:
		# 		mag=mag+i*i
		# 	return math.sqrt(mag)
		# def dot(ddata1,ddata2):
		# 	dot=0
		# 	for i in range(len(ddata1)):
		# 		dot=dot+ddata1[i]*ddata2[i]
		# 	return dot
		# a=mag(comp_data)
		cosine_similarity=[]
		comp_data=data[0] #yo chai vector of given document or select gareko document 
		for i in range(2,len(data)+1):
			i=i-1
			# cosine=dot(comp_data,data[i])/(a*mag(data[i]))*100
			cosine=(1-spatial.distance.cosine(comp_data,data[i]))*100
			cosine_similarity.append([i,cosine])
			
		return cosine_similarity

	def Recommend(self):
		if len(self.all_doc[0])==0:
			return ['error',[0]]
		unique_words=self.tokenize()
		TF_Calc=self.TF(unique_words)
		IDF_Calc=self.IDF(unique_words)
		TF_IDF_Calc=self.TF_IDF(TF_Calc,IDF_Calc)
		# print(TF_Calc)
		cosine=self.cosine_sim(TF_IDF_Calc)
		sorted_data=(sorted(cosine, key=lambda x: x[1],reverse=True))
		result=[]
		score=[]
		def intersect(a,b):
			ins=[]
			for i in a:
				if i in b and i not in ins:
					ins.append(i)
			return ins
		for i in range(len(sorted_data)):
			if sorted_data[i][1]>0:
				doc_no=sorted_data[i][0] #extracting key for document from sorted data
				score.append(sorted_data[i][1])#extracting score for document from sorted data
				result.append(self.actual_doc[doc_no])
				print(intersect(self.all_doc[0],self.all_doc[doc_no]),sorted_data[i][1])
		if len(score)==0:
			return ['NOTHING',[0]] #sapai 0 aayo vani score ni zeroai hunxa ani max 0  nikanu paxxa list ma
		else: 
			return [result,score]

#NAVIE BAYS CLASSIFIER OR MULTINOMIAL NAVIES BAYS CLASSIFIER STARTS HERE
class Navies:
	def __init__(self,input_s):
		data1 = pd.read_csv(open(os.getcwd()+"/myapp/training/long_stop.csv"))
		stop_word= data1["stop"].to_list()
		data = (pd.read_csv(open(os.getcwd()+"/myapp/training/topics.csv")))
		self.topics=["Smartphone","Gamming","Hardware","Software and App","Internet","Security"]
		input_sen=(input_s.lower()).split()
		self.input_sen=[word for word in input_sen if word not in stop_word and word.isalpha()==True]
		overall=[]
		for obj in self.topics:
			term=(data[obj])
			term=(term.dropna()).to_list()
			sen=[s for s in term] 
			word=word_tokenize((" ".join(sen)))
			overall.append([ps.stem(w) for w in word if w not in stop_word and w.isalpha()==True])
		self.overall_term=overall
		# print(self.overall_term)

	def tokenize(self):
		unique_words=[]
		for w in self.overall_term:
			for word in w:
				if word not in unique_words:
					unique_words.append(word)
		# print(unique_words)
		return len(unique_words)

	def word_feq_in_alldoc(self):
		N=[]
		for word in self.input_sen:
			a=0
			# print(ps.stem(word))
			for w in self.overall_term:
				a+=w.count(ps.stem(word))
			# print(word,a)
			N.append(a)
		return N

	def word_feq(self):
		topic_count=[]
		Nk=[]
		i=0
		for topic in self.overall_term:
			# print(topic_term)
			nk=[]
			check=[]
			for word in self.input_sen:
				if ps.stem(word) in topic:
					check.append(ps.stem(word))
				nk.append(topic.count(ps.stem(word)))
			Nk.append(nk)
			print(self.topics[i],"--->",check) #this just for checking
			i+=1
		# print(Nk)
		return Nk

	def navies_bays_likehood(self,voc,N,Nk):
		bays_likehood=[]
		for i in range(len(N)):
			y=N[i]+voc
			formula=[]
			for j in range(len(Nk)):
				x=Nk[j][i]+1
				likehood=x/y
				formula.append(likehood)
			bays_likehood.append(formula)
		return bays_likehood

	def navies_bays_calc(self,bays_likehood,t_doc):
		result=[]
		for i in range(len(bays_likehood[0])):
			prob=1
			for j in range(len(bays_likehood)):
				prob=prob*bays_likehood[j][i]
			result.append((1/t_doc)*prob)
		return result
			
	def navies_bays(self):
		if len(self.input_sen)==0:
			return "unable"
		voc=self.tokenize()
		N=self.word_feq_in_alldoc()
		Nk=self.word_feq()
		bays_likehood=self.navies_bays_likehood(voc,N,Nk)
		t_doc=len(self.topics)
		result=self.navies_bays_calc(bays_likehood,t_doc)
		# print(bays_likehood)
		if len(set(result))==1:
			return "unable"
		high_prob=max(result)
		prediction=[self.topics[i] for i in range(len(result)) if result[i]==high_prob ]
		print(result)
		return prediction