from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import send_news_email


class News(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь')
    date = models.DateTimeField(auto_now=True, verbose_name="Дата")
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(max_length=255, verbose_name='Текст')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ('-date',)


class Subscribe(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='user')
    subscribe = models.ForeignKey(User, verbose_name='Подписка', related_name='subscribe')


class ReadNews(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь')
    news = models.ForeignKey(News, verbose_name='Новость')


@receiver(post_save, sender=News)
def send_email(sender, instance, **kwargs):
    subscribe = Subscribe.objects.filter(subscribe=instance.user)
    if subscribe:
        send_news_email(instance, subscribe)
