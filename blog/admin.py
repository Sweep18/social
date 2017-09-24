from django.contrib import admin

from .models import News


class NewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'title', 'text')
    list_display_links = ('user', 'date', 'title', 'text')
    list_filter = ('date',)


admin.site.register(News, NewsAdmin)
