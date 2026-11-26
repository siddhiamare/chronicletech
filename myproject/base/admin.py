from django.contrib import admin
from .models import Category, Article, Event


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'badge_color', 'article_count', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = 'Articles'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'read_time', 'is_featured', 'views_count', 'published_at')
    list_filter = ('category', 'is_featured', 'published_at')
    search_fields = ('title', 'content', 'short_desc', 'author')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ('-published_at',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_str', 'location', 'category_tag', 'is_featured')
    list_filter = ('category_tag', 'is_featured')
    search_fields = ('title', 'location', 'description')
