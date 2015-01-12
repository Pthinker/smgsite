from glob import glob


from smgsite.pages.models import Template, Directory, Page

from django.contrib import admin
from django import forms
from django.conf import settings


class TemplateAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)
	fields = ('name',)

admin.site.register(Template, TemplateAdmin)


class DirectoryAdmin(admin.ModelAdmin):
	list_display = ('directory', 'template')
	search_fields = ('directory',)
	fields = ('directory', 'template')

admin.site.register(Directory, DirectoryAdmin)


ROOT_TEMPLATE_DIR = '%s/templates/' % settings.ROOT_DIR

def get_template_choices():
    # get selection of templates for pages
    res = [('','Select a Template')]
    for f in glob('%spages/*.html' % ROOT_TEMPLATE_DIR):
        res.append((f.replace(ROOT_TEMPLATE_DIR, ''), f.replace(ROOT_TEMPLATE_DIR, '')))
    return res


def clean_unique(form, field, exclude_initial=True, 
                 format="The %(field)s %(value)s has already been taken."):
    value = form.cleaned_data.get(field)
    if value:
        qs = form._meta.model._default_manager.filter(**{field:value})
        if exclude_initial and form.initial:
            initial_value = form.initial.get(field)
            qs = qs.exclude(**{field:initial_value})
        if qs.count() > 0:
            raise forms.ValidationError(format % {'field':field, 'value':value})
    return value

class PageAdminForm(forms.ModelForm):

	class Meta:
		model = Page
		
		widgets = {
            'template_name': forms.widgets.Select(choices=get_template_choices()),
        }

	"""
	def clean_urlname(self):
		value = self.cleaned_data['urlname']
		if value.find('/') != -1:
			raise forms.ValidationError('The urlname for a Page must not contain any forward slash ("/") characters.')
		return value
	"""

	def clean_url(self):
		"""
		Make sure that the URL is unique
		"""
		return clean_unique(self, 'url')


class PageAdmin(admin.ModelAdmin):
	form = PageAdminForm
	list_display = ('title', 'directory', 'urlname', 'url', 'template_name', 'active')
	list_filter = ('active', 'directory')
	list_editable = ('active',)

	search_fields = ('title', 'urlname', 'content')



	fieldsets = (
		('Name', {
			'fields' : ('title',)
		}),
		('Location (legacy options)', {
			'classes': ('collapse',),
			'fields': ('directory', 'urlname')
		}),
		('URL and Template', {
			'classes': 'wide',
			'fields': ('url', 'template_name')
		}),
		('Page Content', {
			'classes': 'wide',
			'fields': ('content', 'marketing_banner')
		}),
		('Options', {
			'fields' : ('keywords', 'meta_description', 'active'),
		})
	)

admin.site.register(Page, PageAdmin)
