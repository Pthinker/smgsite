from smgsite.healthday.models import Article, Category
from django.contrib import admin
from smgsite.settings import MEDIA_URL

class ArticleAdmin(admin.ModelAdmin):
	list_display = ('headline', 'posting_time')
	list_filter = ('topics',)
	search_fields = ('headline',)
	fieldsets = (
			('Article', {
				'fields': ('headline', 'byline', 'topics'),
			}),
			('Body', {
				'fields': ('body',)
			})
	)
	filter_horizontal = ('topics',)

admin.site.register(Article, ArticleAdmin)


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('category',)
	search_fields = ('category',)
	fields = ('category', 'description', 'topics')
	filter_horizontal = ('topics',)

admin.site.register(Category, CategoryAdmin)
