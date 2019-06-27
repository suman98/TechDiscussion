"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('logout/',views.logout,name='logout'),
    path('Notification/',views.Notification,name='Notification'),
    path('report/',views.report,name='report'),
    path('check_login/',views.check_login,name='check_login'),
    path('ask/',views.ask,name='ask'),
    path('view_item',views.view_item,name='view_item'),
    path('signup/',views.signup,name='signup'),
    path('like_view/',views.like_view,name='like_view'),
    path('profile/',views.profile,name='profile'),
    path('search/',views.search,name='search'),
    path('post_ans/',views.post_ans,name='post_ans'),
    path('message/',views.message,name='message'),
    path('delete/',views.delete,name='delete'),
    path('ans_sort',views.ans_sort,name='ans_sort'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)