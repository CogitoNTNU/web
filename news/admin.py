from django.contrib import admin

from news.models import Article, Event, FiletoArticle

class FileInline(admin.TabularInline):
    model=FiletoArticle
    extra=1

class ArticleAdmin(admin.ModelAdmin):
    inlines = [FileInline]
    #Defines the files attached to the article
    fieldsets = [
        ('Title', {'fields':['title']}),
        ('Ingress', {'fields': ['ingress']}),
        ('Content', {'fields': ['content']}),
        ('Banner', {'fields': ['banner']}),
        ('Published', {'fields': ['published']}),
        ('Pinned', {'fields': ['pinned']})
    ]
admin.site.register(Article, ArticleAdmin)
admin.site.register(Event)

