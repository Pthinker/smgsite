from smgsite.services.models import (Template, Service, Link_Nav, Link_Body, 
    URLAlias, Location, ServiceGroup, ServiceGroupDetail)
from django.contrib import admin



class ServiceGroupDetailInline(admin.TabularInline):
    model = ServiceGroupDetail
    extra = 1
    #max_num=0


class ServiceGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'order')
    prepopulated_fields = {"urlname": ("name",)}
    #list_filter = ('services',)
    inlines = (ServiceGroupDetailInline,)

admin.site.register(ServiceGroup, ServiceGroupAdmin)

class TemplateAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)
	fields = ('name',)

admin.site.register(Template, TemplateAdmin)


class LinkNavInline(admin.TabularInline):
    model = Link_Nav
    raw_id_fields = ('resource',)
    extra = 3


class LinkBodyInline(admin.TabularInline):
    model = Link_Body
    raw_id_fields = ('resource',)
    extra = 3


class LocationInline(admin.TabularInline):
    model = Location
    extra = 2


class ServiceAdmin(admin.ModelAdmin):
	list_display = ('name', 'changes', 'active', 'date_added',)
	list_filter = ('active', 'servicegroupdetail__servicegroup__name')
	search_fields = ('name',)

	fieldsets = (
		('Name', {
			'classes': ('collapse',),
			'fields' : ('template', 'name', 'practitioner_name', 'practitioner_group', 'description_short', 'meta_description', 'seo_keywords'),
		}),
		('Contact', {
			'classes': ('collapse',),
			'fields' : ('phone', 'related_services'),
		}),
		('Page Content', {
			'classes': ('wide',),
			'fields': ('content', 'offerings', 'learn_more', 'patient_tools', 'blog', 'marketing_banner')
		}),
        ('Media', {
            'classes': ('wide',),
            'fields': ('large_image', 'small_image', )
        }),
		('Options', {
			'classes': ('collapse',),
			'fields' : ('keywords', 'urlname', 'aliases', 'active'),
		})
	)
	filter_horizontal = ('related_services', 'aliases')
	inlines = (LocationInline, LinkNavInline, LinkBodyInline,)

admin.site.register(Service, ServiceAdmin)


class URLAliasAdmin(admin.ModelAdmin):
	search_fields = ('urlname',)
	fields = ('urlname',)

admin.site.register(URLAlias, URLAliasAdmin)
