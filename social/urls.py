"""social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.contrib.auth import views as auth_views


from blog import views

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.MainPage.as_view(), name='main_page'),
    url(r'^add/$', views.AddNews.as_view(), name='add_news'),
    url(r'^all/$', views.AllUsers.as_view(), name='all_users'),
    url(r'^(?P<pk>[0-9]+)/$', views.UserBlog.as_view(), name='user_blog'),
    url(r'^news/$', views.NewsPage.as_view(), name='news_page'),
    url(r'^news/(?P<pk>[0-9]+)/$', views.SingleNews.as_view(), name='single_news'),
    url(r'^news/(?P<news_id>[0-9]+)/read/$', views.read_news, name='read_news'),
]
