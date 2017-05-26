"""OJ_Test_Login URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app_user import views as user_view
from app_problem import views as problem_view

urlpatterns = [
    url(r'^$', user_view.index),
    url(r'^accounts/login/$', user_view.login),
    url(r'^accounts/register/$', user_view.register),
    url(r'^accounts/logout/$', user_view.logout),
    url(r'^accounts/userHomePage/$', user_view.changePassword),

    url(r'^problem/\d{1,2}/$', problem_view.problem),
    url(r'^problem/\d{4}/$', problem_view.submit),

    url(r'^problem/\d{1,3}/\d{4}/$', problem_view.submit),

    url(r'^ranking/$', problem_view.ranking),

    url(r'^submit/\d{1,3}/$', problem_view.submit_home_page),
    url(r'^submit/\d{1,3}/\d{1,3}/$', problem_view.view_submit_code),

    url(r'^admin/', admin.site.urls),
]
