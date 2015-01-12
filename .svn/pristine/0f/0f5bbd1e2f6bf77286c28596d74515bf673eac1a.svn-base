from smgsite.blogs.models import Blog, BlogEntry, BlogSection, BlogEntrySection
from django.contrib import admin
from smgsite.settings import MEDIA_URL

class BlogSectionInline(admin.TabularInline):
	model = BlogSection
	extra = 2

class BlogAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)
	fieldsets = (
		('Name', {
			'classes': 'wide',
			'fields': ('name',)
		}),
		('Authors', {
			'classes': 'wide',
			'fields': ('authors', 'editors')
		}),
		('Options', {
			'fields' : ('image', 'blurb', 'keywords', 'meta_description', 'urlname', 'active'),
		})
	)
	inlines = (
		BlogSectionInline,
	)
	filter_horizontal = ('authors', 'editors')

admin.site.register(Blog, BlogAdmin)


class BlogEntrySectionInline(admin.TabularInline):
	model = BlogEntrySection
	extra = 2

	def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
		field = super(BlogEntrySectionInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

		if db_field.name == 'section':
			if request._obj_ is not None:
				field.queryset = field.queryset.filter(blog=request._obj_.blog.pk)
			else:
				field.queryset = field.queryset.none()

		return field

class BlogEntryAdmin(admin.ModelAdmin):
	list_display = ('author', 'blog', 'title', 'postdate')
	list_filter = ('blog',)
	search_fields = ('title', 'byline')
	fieldsets = (
		('Date', {
			'classes': 'wide',
			'fields': ('posting_time', 'display_time')
		}),
		('Name', {
			'classes': 'wide',
			'fields': ('blog', 'title', 'byline', 'byline_link', 'author', 'reviewed_by', 'reviewed_by_link')
		}),
		('Content', {
			'classes': 'wide',
			'fields': ('body',)
		}),
		('Options', {
			'fields' : ('keywords', 'urlname', 'active', 'exclude_from_archiving'),
		})
	)
	inlines = (
		BlogEntrySectionInline,
	)

	def get_form(self, request, obj=None, **kwargs):
		request._obj_ = obj
		return super(BlogEntryAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(BlogEntry, BlogEntryAdmin)
