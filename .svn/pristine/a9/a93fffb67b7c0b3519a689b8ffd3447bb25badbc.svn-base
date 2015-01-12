from smgsite.careers.models import Career
from django.contrib import admin
from smgsite.settings import MEDIA_URL

class CareerAdmin(admin.ModelAdmin):
	list_display = ('job_title', 'date_posted', 'department', 'changes')
	list_filter = ('department', 'shift_type', 'shift_time')
	search_fields = ('job_title', 'department')
	fieldsets = (
		('Job', {
			'fields' : ('job_title', 'position_number', 'description', 'requirements'),
		}),
		('Information', {
			'fields' : ('department', 'service', 'location', 'other_location', 'benefits'),
		}),
		('Times', {
			'classes': 'wide',
			'fields': ('shift', 'shift_type', 'shift_time', 'hours')
		}),
		('Posting', {
			'classes': 'wide',
			'fields': ('date_posted', 'status')
		})
	)

admin.site.register(Career, CareerAdmin)
