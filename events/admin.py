from smgsite.events.models import Event, EventBanner, Registration, Referrer, Class, Eventtime
from django.contrib import admin
from smgsite.settings import MEDIA_URL


class EventtimeInline(admin.TabularInline):
    model = Eventtime
    extra = 2


class EventAdmin(admin.ModelAdmin):
	list_display = ('title', 'most_recent', 'changes')
	list_filter = ('title',)
	search_fields = ('title',)
	fieldsets = (
		('Event', {
			'fields' : ('title', 'event_type', 'short_description', 'description', 'meta_description', 'service', 'related_services', 'icon', 'exclude_from_registration'),
		}),
		('Status', {
			'fields' : ('active', 'notification'),
		}),
		('Presenters', {
			'classes': 'wide',
			'fields': ('local_presenters', 'other_presenter', 'presenter_url', 'sponsored_by', 'sponsor_url')
		}),
		('Location', {
			'classes': 'wide',
			'fields': ('location', 'room', 'other_location')
		}),
		('Website', {
			'classes': 'wide',
			'fields': ('original_image', 'urlname', 'keywords')
		})
	)
	inlines = (
		EventtimeInline,
	)
	filter_horizontal = ('local_presenters', 'related_services')

admin.site.register(Event, EventAdmin)


class EventBannerAdmin(admin.ModelAdmin):
	list_display = ('name', 'active', 'date_added')
	ordering = ('-date_added', 'name')
	fieldsets = (
			('Banner Information', {
				'classes': 'wide',
				'fields': ('active', 'name', 'image', 'link')
				}),
			)

admin.site.register(EventBanner, EventBannerAdmin)


class ClassAdmin(admin.ModelAdmin):
	list_display = ('title', 'startdate', 'starttime', 'changes')
	list_filter = ('startdate', 'starttime')
	search_fields = ('title',)
	fieldsets = (
		('Class', {
			'fields' : ('title', 'short_description', 'description', 'meta_description', 'service', 'related_services'),
		}),
		('Status', {
			'fields' : ('active',),
		}),
		('Times', {
			'fields' : ('startdate', 'starttime', 'enddate', 'endtime', 'cancellations'),
		}),
		('Days', {
			'fields' : ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'),
		}),
		('Presenters', {
			'classes': 'wide',
			'fields': ('local_presenters', 'other_presenter', 'presenter_url', 'sponsored_by', 'sponsor_url')
		}),
		('Location', {
			'classes': 'wide',
			'fields': ('location', 'room', 'other_location')
		}),
		('Website', {
			'classes': 'wide',
			'fields': ('original_image', 'urlname', 'keywords')
		})
	)
	filter_horizontal = ('local_presenters', 'related_services')

admin.site.register(Class, ClassAdmin)


class RegistrationAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'email', 'city', 'state', 'signup_date')
	search_fields = ('last_name', 'first_name', 'email', 'city', 'state',)
	ordering = ('-signup_date',)
	fieldsets = (
		('Registration information', {
			'classes': 'wide',
			'fields': ('eventtimes', 'first_name', 'last_name', 'age', 'city', 'state', 'zipcode')
		}),
		('Contact information', {
			'classes': 'wide',
			'fields': ('email', 'main_phone', 'alt_phone', 'sendmail')
		}),
		('Administrative', {
			'classes': 'wide',
			'fields': ('status', 'referrer', 'entered_by')
		})
	)

admin.site.register(Registration, RegistrationAdmin)


class ReferrerAdmin(admin.ModelAdmin):
        list_display = ('name', 'order')
        search_fields = ('name', 'order')
	ordering = ('order',)
        fields = ('name', 'order')

admin.site.register(Referrer, ReferrerAdmin)

