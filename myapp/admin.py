from django.contrib import admin
from .models import Question,User,Answer,Report,Like_view
class QuestionAdmin(admin.ModelAdmin):
	list_display=['user_id','topics','question','description']
	
class UserAdmin(admin.ModelAdmin):
	list_display=['user_id','Fname','Lname','Address','email','Interest','profile']
class AnswerAdmin(admin.ModelAdmin):
	list_display=['user_id','question_id','answer','uploaded_at']
class ReportAdmin(admin.ModelAdmin):
	list_display=['question_id','user_id','message']
	def delete_model(self,request,queryset):
		Question_data=Question()
		for obj in queryset:
			Question_data.question_id=obj.question_id.question_id
			Question_data.delete()
	actions=[delete_model]
	delete_model.short_description = "Delete Post"
class LikeAdmin(admin.ModelAdmin):
	list_display=['question_id','user_id','type1']
# Register your models here.
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer,AnswerAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Report,ReportAdmin)
admin.site.register(Like_view,LikeAdmin)
