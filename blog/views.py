from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from .models import News, Subscribe, ReadNews
from .forms import NewsForm, SubscribeForm


# Главная страница
class MainPage(LoginRequiredMixin, ListView):
    context_object_name = 'main'
    template_name = 'blog/main_page.html'
    model = News

    def get_queryset(self):
        return News.objects.filter(user=self.request.user)


# Добавить новость
class AddNews(LoginRequiredMixin, FormView):
    form_class = NewsForm
    template_name = 'blog/add_news.html'
    success_url = '/'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.user = self.request.user
        news.save()
        return super(AddNews, self).form_valid(form)


# Все блоги
class AllUsers(LoginRequiredMixin, ListView):
    context_object_name = 'users'
    template_name = 'blog/all_users.html'
    model = User

    def get_queryset(self):
        return User.objects.all().exclude(id=self.request.user.id)


# Блог пользователя
class UserBlog(LoginRequiredMixin, FormView):
    template_name = 'blog/user_blog.html'
    form_class = SubscribeForm

    def get_context_data(self, **kwargs):
        context = super(UserBlog, self).get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs['pk'])
        context['blogs'] = News.objects.filter(user=user)
        context['user'] = user
        stat_subscribe = Subscribe.objects.filter(user=self.request.user, subscribe=user.id)
        if stat_subscribe:
            context['stat_subscribe'] = True
        return context

    def get_initial(self):
        initial = super(UserBlog, self).get_initial()
        initial['user'] = self.request.user
        initial['subscribe'] = self.kwargs['pk']
        return initial

    def form_valid(self, form):
        user = form.cleaned_data['user']
        subscribe = form.cleaned_data['subscribe']
        if 'delete' in self.request.POST:
            Subscribe.objects.get(user=user, subscribe=subscribe).delete()
            readnews = ReadNews.objects.filter(user=self.request.user)
            for read in readnews:
                if read.news.user == subscribe:
                    ReadNews.objects.get(user=self.request.user, news=read.news).delete()
        else:
            form.save()
        return super(UserBlog, self).form_valid(form)

    def get_success_url(self):
        return reverse('user_blog', kwargs={'pk': self.kwargs['pk']})


# Все новости
class NewsPage(LoginRequiredMixin, ListView):
    context_object_name = 'news'
    template_name = 'blog/news.html'
    model = News

    def get_context_data(self, **kwargs):
        subscribe_list = []
        read_list = []
        context = super(NewsPage, self).get_context_data(**kwargs)
        subscribe = Subscribe.objects.filter(user=self.request.user)
        for sub in subscribe:
            subscribe_list.append(sub.subscribe.id)
        context['subscribe'] = subscribe_list
        readnews = ReadNews.objects.filter(user=self.request.user)
        for read in readnews:
            read_list.append(read.news.id)
        context['read'] = read_list
        return context


# Одна новость
class SingleNews(LoginRequiredMixin, DetailView):
    template_name = 'blog/single_news.html'
    context_object_name = 'news'
    model = News


# Пометить новость прочитанной
@login_required()
def read_news(request, news_id):
    news = News.objects.get(id=news_id)
    ReadNews.objects.create(user=request.user, news=news)
    return HttpResponseRedirect("/news/")
