from smgsite.doctors.models import (Doctor, Degree, Degree_letters, Accreditation, 
	Accreditation_name, Link_Nav, Featured, Location, Specialty, Hospital, Language)
from smgsite.doctors.forms import DoctorAdminForm
from django.contrib import admin
from django import forms
from django.db.models import Q
from smgsite.settings import MEDIA_URL

class Degree_lettersAdmin(admin.ModelAdmin):
	list_display = ('letters', 'sort_order')
	search_fields = ('letters', 'sort_order')
	fields = ('letters', 'sort_order', 'description_short', 'description_long')

admin.site.register(Degree_letters, Degree_lettersAdmin)

class LanguageAdmin(admin.ModelAdmin):
	model = Language

admin.site.register(Language, LanguageAdmin)

class DegreeInline(admin.TabularInline):
    model = Degree


class Accreditation_nameAdmin(admin.ModelAdmin):
	list_display = ('name', 'sort_order')
	search_fields = ('name', 'sort_order')
	fields = ('name', 'name_plural', 'sort_order')

admin.site.register(Accreditation_name, Accreditation_nameAdmin)


class DegreeInline(admin.TabularInline):
    model = Degree
    extra = 2


class AccreditationInline(admin.TabularInline):
    model = Accreditation
    extra = 2


class LinkInline(admin.TabularInline):
    model = Link_Nav
    raw_id_fields = ('resource',)
    extra = 3


class LocationInline(admin.TabularInline):
    model = Location
    extra = 2


class DoctorAdmin(admin.ModelAdmin):
	list_display = ('list_name', 'changes', 'active', 'date_added')
	list_filter = ('active', 'letters')
	search_fields = ('first_name', 'last_name')
        list_per_page = 1000
	fieldsets = (
		('Name', {
			'classes': 'wide',
			'fields': ('prefix', 'first_name', 'middle_name', 'last_name', 'suffix', 'letters', 'gender', 'status')
		}),
		('Contact', {
			'classes': 'wide',
			'fields': ('email', 'phone', 'phone_note', 'accepting_flag', 'accepting', 'hospitals', 'languages')
		}),
		('Image', {
			'classes': 'wide',
			'fields': ('original_image', 'cropped_image')
		}),
		('Services & Specialties', {
			'classes': 'wide',
			'fields': ('title_service', 'services', 'specialties')
		}),
		('Personal Touch', {
			'classes': 'wide',
			'fields': ('touch', 'blog')
		}),
		('Options', {
			'fields' : ('keywords', 'meta_description', 'seo_keywords', 'urlname', 'active', 'exclude_from_index', 'patient_portal', 'appointments', 'portal_refill', 'email_staff', 'lab_results', 'portal_accounts', 'marketing_banner'),
		})
	)
	inlines = (
		LocationInline, DegreeInline, AccreditationInline, LinkInline,
	)
	filter_horizontal = ('services', 'specialties',)
	form = DoctorAdminForm

	def save_model(self, request, obj, form, change):
		if obj.id: # A reindex can only happen for existing doctors
			form.save_m2m()
			#Doctor.qa_objects.get(id=obj.id).index(post=True) # Force a reindex of m2m fields before saving
			obj.save(preview=True)
		else:
			obj.save(preview=True)
			form.save_m2m()

admin.site.register(Doctor, DoctorAdmin)


class MyFeaturedAdminForm(forms.ModelForm):
	class Meta:
		model = Featured

	def clean(self):
		startdate = self.cleaned_data['startdate']
		enddate = self.cleaned_data['enddate']
		doctor = self.cleaned_data['doctor']
		if startdate > enddate:
			raise forms.ValidationError('The date range you selected has a start date after the end date. Please go back and correct the dates.')
		existing = Featured.all_objects.filter(Q(startdate__gte=startdate, startdate__lte=enddate) | Q(enddate__gte=startdate, enddate__lte=enddate)).exclude(doctor__pk=doctor.pk)
		if existing:
			raise forms.ValidationError('The date range you entered conflicts with the dates for another featured practitioner. Please adjust the date range on this form, or else review and modify the dates for the conflicting practitioner(s) %s. If you have deleted the current featured practitioner, you must approve that action before attempting to save your current change.' % (existing[1:]))
		return self.cleaned_data


class FeaturedAdmin(admin.ModelAdmin):
	form = MyFeaturedAdminForm
	list_display = ('doctor', 'startdate', 'enddate')
	search_fields = ('doctor__last_name', 'doctor__first_name')
	fields = ('doctor', 'startdate', 'enddate', 'blurb')

admin.site.register(Featured, FeaturedAdmin)

class SpecialtyAdmin(admin.ModelAdmin):
	list_display = ('specialty',)
	search_fields = ('specialty',)
	fields = ('specialty',)

admin.site.register(Specialty, SpecialtyAdmin)

class HospitalAdmin(admin.ModelAdmin):
	list_display = ('hospital',)
	search_fields = ('hospital',)
	fields = ('hospital',)

admin.site.register(Hospital, HospitalAdmin)
