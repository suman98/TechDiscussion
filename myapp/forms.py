from django import forms
from .models import User,Question,Answer
class UserForm(forms.ModelForm):
	class Meta:
		model= User
		fields=('user_id','Fname','Lname','Address','email','password','Interest','profile',)
		widgets = {
        'password': forms.PasswordInput(),
        'email': forms.EmailInput(),
    }
class QuestionForm(forms.ModelForm):
	class Meta:
		model= Question
		fields=('topics','question','description','question_img')
		widgets = {
            'question': forms.TextInput(attrs={'placeholder': 'Enter the valid question start with What , Why, How,...etc'}),
            'description': forms.Textarea(
                attrs={'placeholder': 'Please provide the necessary description of yours problem if required..'}),
        }
	
