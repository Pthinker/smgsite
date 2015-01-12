from django import forms
from django.contrib import admin

from smgsite.site.models import Location, Resource, MediaCategory, Image
from smgsite.site.models import WeekdayHours, SaturdayHours, SundayHours
from smgsite.site.models import MediaFile, HomepageImage, VideoTemplate
from smgsite.site.models import Unsubscribe, ImageSlide

from smgsite.settings import MEDIA_URL


class ImageSlideAdmin(admin.ModelAdmin):
	list_display = ('name', 'display_time', 'order', 'active', 'url', 'target', )
	list_filter = ('active',)
	list_editable = ('order', 'active',)
	ordering = ['-display_time']

admin.site.register(ImageSlide, ImageSlideAdmin)


class WeekdayHoursInline(admin.TabularInline):
    model = WeekdayHours

class SaturdayHoursInline(admin.TabularInline):
    model = SaturdayHours

class SundayHoursInline(admin.TabularInline):
    model = SundayHours


class LocationAdmin(admin.ModelAdmin):
	list_display = ('name', 'order', 'description', 'address', 'city', 'meta_description')
	search_fields = ('name', 'order', 'description', 'address', 'city', 'meta_description')
	inlines = (
			WeekdayHoursInline,
			SaturdayHoursInline,
			SundayHoursInline,
	)

admin.site.register(Location, LocationAdmin)


class ResourceAdmin(admin.ModelAdmin):
	list_display = ('name', 'id', 'url')
	search_fields = ('name', 'id', 'url')

admin.site.register(Resource, ResourceAdmin)


class MediaCategoryAdmin(admin.ModelAdmin):
	list_display = ('category',)
	search_fields = ('category',)

admin.site.register(MediaCategory, MediaCategoryAdmin)


class ImageAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)

admin.site.register(Image, ImageAdmin)


class MediaFileAdmin(admin.ModelAdmin):
	list_display = ('mediafile',)
	search_fields = ('mediafile',)

admin.site.register(MediaFile, ImageAdmin)


class HomepageImageAdmin(admin.ModelAdmin):
	list_display = ('location',)
	search_fields = ('location',)

admin.site.register(HomepageImage, HomepageImageAdmin)

class VideoTemplateAdmin(admin.ModelAdmin):
	list_display = ('location',)
	search_fields = ('location',)

admin.site.register(VideoTemplate, VideoTemplateAdmin)

class UnsubscribeAdmin(admin.ModelAdmin):
	list_display = ('first_name', 'last_name')
	search_fields = ('first_name', 'last_name', 'city')

admin.site.register(Unsubscribe, UnsubscribeAdmin)

