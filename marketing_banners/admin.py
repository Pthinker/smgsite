from smgsite.marketing_banners.models import Resource, MarketingBanner, MBGroup
from django.contrib import admin
from smgsite.settings import MEDIA_URL

class ResourceAdmin(admin.ModelAdmin):
	list_display = ('name', 'url')
	search_fields = ('name',)

admin.site.register(Resource, ResourceAdmin)


class MarketingBannerAdmin(admin.ModelAdmin):
	list_display = ('name', 'active', 'date_added')
	search_fields = ('name',)
	date_hierarchy = 'date_added'

admin.site.register(MarketingBanner, MarketingBannerAdmin)


class MBGroupAdmin(admin.ModelAdmin):
	list_display = ('name', 'active', 'start_date', 'end_date')
	search_fields = ('name',)
	fieldsets = (
		(None, {
			'fields': ('name', 'banners', 'urls')
		}),
		('Advanced Options', {
			'fields': ('active',)
		})
	)
	filter_horizontal = ('banners',)

admin.site.register(MBGroup, MBGroupAdmin)
