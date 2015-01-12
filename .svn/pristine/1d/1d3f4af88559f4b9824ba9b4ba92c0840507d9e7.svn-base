from smgsite.mysmg.models import User
from django.contrib import admin
from smgsite.settings import MEDIA_URL

class UserAdmin(admin.ModelAdmin):
	list_display = ('fullname','username','phone','zipcode')
	list_filter = ('contact',)
	search_fields = ('username','first_name','middle_name','last_name','phone','zipcode')
	fieldsets = (
		('Name', {
			'fields': ('username','first_name','middle_name','last_name',)
		}),
		('Info', {
			'fields': ('phone', 'zipcode','security_question','security_answer','contact')
		}),
		('Password', {
			'fields': ('password',)
		}),
	)

admin.site.register(User, UserAdmin)
