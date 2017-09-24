from django.core.mail import send_mail
from django.conf import settings


def send_news_email(news, subscribe):
    email_list = []
    for sub in subscribe:
        email_list.append(sub.user.email)
    link = 'http://%s/news/%s/' % (settings.DOMAIN, str(news.id))
    send_mail('Новая запись', 'Добавлена запись: ' + link, 'from@example.com', email_list, fail_silently=False)
