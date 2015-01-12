from smgsite.articles.models import Article, PressRelease, Feature, Recipe, URLAlias, PDF
from smgsite.articles.models import MediaResult, TrendingTopic
from django.contrib import admin
from django import forms
from django.forms.util import flatatt
from smgsite.settings import MEDIA_URL

import re

"""
class ArticleAdminForm(forms.ModelForm):
	class Meta:
		model = Article
	
	def __init__(self, *args, **kwargs):
		super(ArticleAdminForm, self).__init__(*args, **kwargs)
		w = self.fields['leader_promo'].widget
		choices = [(0, 'Off')]
		for key, value in Article.PROMO:
			if key != 0 and ((self.initial.has_key('leader_promo') and key == self.initial['leader_promo']) or not Article.all_objects.filter(leader_promo=key)):
				choices.append((key,value))
		w.choices = choices
		w = self.fields['headline_promo'].widget
		choices = [(0, 'Off')]
		for key, value in Article.PROMO:
			if key != 0 and ((self.initial.has_key('headline_promo') and key == self.initial['headline_promo']) or not Article.all_objects.filter(headline_promo=key)):
				choices.append((key,value))
		w.choices = choices
	
	def clean_leader_promo(self):
		value = self.cleaned_data['leader_promo']
		if self.initial and 'leader_promo' in self.changed_data and value == 0:
			leaders = Article.all_objects.filter(leader_promo__gt=0)
			if len(leaders) <= 1:
				raise forms.ValidationError('This is the last Homepage Leader news story. It cannot be deleted or reset as a non-leader story until there is another Leader news story. There must always be at least one Leader for the Homepage.')
		if 'leader_promo' in self.changed_data and value != 0:
			promos = Article.all_objects.filter(leader_promo__gt=0)
			for promo in promos:
				if promo.leader_promo == value:
					raise forms.ValidationError('Promo position %s has already been selected. Please select a different position.' % value)
		return value
	def clean_headline_promo(self):
		value = self.cleaned_data['headline_promo']
		if self.initial and 'headline_promo' in self.changed_data:
			leader = self.cleaned_data['leader_promo']
			if leader and leader != 0 and value != 0:
				raise forms.ValidationError('Headline promo position can only be set for articles that are not leader articles. Leader promo above must be Off in order to set the headline position.')
			if 'headline_promo' in self.changed_data and value != 0:
				promos = Article.all_objects.filter(headline_promo__gt=0)
				for promo in promos:
					if promo.headline_promo == value:
						raise forms.ValidationError('Promo position %s has already been selected. Please select a different position.' % value)
		return value
"""
def make_inactive(modeladmin, request, queryset):
    queryset.update(active='0')
make_inactive.short_description = "Set selected articles to inactive"

def make_active(modeladmin, request, queryset):
    queryset.update(active='1')
make_active.short_description = "Set selected articles to active"

class ArticleAdmin(admin.ModelAdmin):
	#form = ArticleAdminForm
	list_display = ('posting_time', 'headline', 'headline_promo', 'active')
	list_filter = ('posting_time', 'headline_promo', 'active')
	search_fields = ('headline',)
	fieldsets = (
		('Article', {
			'fields' : ('active', 'posting_time', 'display_time', 'headline', 'byline', 'byline_link', 'reviewed_by', 'reviewed_by_link', 'urlname', 'aliases', 'keywords', 'meta_description'),
		}),
		('Content', {
			'classes': ('wide',),
			'fields': ('original_image', 'blurb', 'content', 'marketing_banner'),
		})
	)
	filter_horizontal = ('aliases',)
	actions = [make_inactive, make_active]
	list_editable = ('headline', 'active', 'headline_promo',)

admin.site.register(Article, ArticleAdmin)




class PressReleaseAdmin(admin.ModelAdmin):
	list_display = ('headline', 'posting_time')
	list_filter = ('posting_time',)
	search_fields = ('headline',)
	fieldsets = (
		('Press Release', {
			'fields' : ('active', 'posting_time', 'display_time', 'headline', 'byline', 'urlname', 'aliases', 'keywords', 'meta_description'),
		}),
		('Content', {
			'classes': ('wide',),
			'fields': ('use_boilerplate', 'content',),
		})
	)
	filter_horizontal = ('aliases',)

admin.site.register(PressRelease, PressReleaseAdmin)


class FeatureAdmin(admin.ModelAdmin):
	list_display = ('content_type', 'headline', 'posting_time',)
	list_filter = ('content_type', 'posting_time',)
	search_fields = ('content_type', 'headline',)
	fieldsets = (
		('Feature', {
			'fields' : ('content_type', 'active', 'posting_time', 'display_time', 'headline', 'byline', 'byline_link', 'reviewed_by', 'reviewed_by_link', 'urlname', 'aliases', 'keywords', 'meta_description'),
		}),
		('Content', {
			'classes': ('wide',),
			'fields': ('content', 'related_recipes',),
		})
	)
	filter_horizontal = ('aliases',)

admin.site.register(Feature, FeatureAdmin)


num_re = re.compile(r'^\d{0,5}$')


class MyRecipeAdminForm(forms.ModelForm):
	class Meta:
		model = Recipe

	def clean_num_servings(self):
		if not num_re.match(self.cleaned_data["num_servings"]):
			raise forms.ValidationError("Invalid number entered")
		return self.cleaned_data["num_servings"]
		if not num_re.match(self.cleaned_data["calories"]):
			raise forms.ValidationError("Invalid number entered")
		return self.cleaned_data["calories"]
		if not num_re.match(self.cleaned_data["fat_cals"]):
			raise forms.ValidationError("Invalid number entered")
		return self.cleaned_data["fat_cals"]
		if not num_re.match(self.cleaned_data["total_fat"]):
			raise forms.ValidationError("Invalid number entered")
		return self.cleaned_data["total_fat"]
		if not num_re.match(self.cleaned_data["saturated_fat"]):
			raise forms.ValidationError("Invalid number entered")
		return self.cleaned_data["saturated_fat"]
		if not num_re.match(self.cleaned_data["trans_fat"]):
			raise forms.ValidationError("Invalid number entered")
		return self.cleaned_data["trans_fat"]
		if not num_re.match(self.cleaned_data["cholesterol"]):
			raise forms.ValidationError("Invalid number entered")
		return self.cleaned_data["cholesterol"]
		if not num_re.match(self.cleaned_data["sodium"]):
			raise forms.ValidationError("Invalid number entered")
		return self.cleaned_data["sodium"]
		if not num_re.match(self.cleaned_data["total_carbs"]):
			raise forms.ValidationError("Invalid number entered")
		return self.cleaned_data["total_carbs"]
		if not num_re.match(self.cleaned_data["dietary_fiber"]):
			raise forms.ValidationError("Invalid number entered")
		return self.cleaned_data["dietary_fiber"]
		if not num_re.match(self.cleaned_data["sugars"]):
			raise forms.ValidationError("Invalid number entered")
		return self.cleaned_data["sugars"]
		if not num_re.match(self.cleaned_data["protein"]):
			raise forms.ValidationError("Invalid number entered")
		return self.cleaned_data["protein"]
		if not num_re.match(self.cleaned_data["vit_a"]):
			raise forms.ValidationError("Invalid number entered")
		return self.cleaned_data["vit_a"]
		if not num_re.match(self.cleaned_data["vit_c"]):
			raise forms.ValidationError("Invalid number entered")
		return self.cleaned_data["vit_c"]
		if not num_re.match(self.cleaned_data["calcium"]):
			raise forms.ValidationError("Invalid number entered")
		return self.cleaned_data["calcium"]
		if not num_re.match(self.cleaned_data["iron"]):
			raise forms.ValidationError("Invalid number entered")
		return self.cleaned_data["iron"]


class RecipeAdmin(admin.ModelAdmin):
	form = MyRecipeAdminForm
	list_display = ('title', 'posting_time',)
	list_filter = ('posting_time',)
	search_fields = ('title',)
	fieldsets = (
		('Feature', {
			'fields' : ('active', 'posting_time', 'display_time', 'featured', 'title', 'byline', 'byline_link', 'reviewed_by', 'reviewed_by_link', 'urlname', 'aliases', 'keywords', 'meta_description'),
			}),
		('Content', {
			'classes': ('wide',),
			'fields': ('recipe_type', 'original_image', 'description', 'ingredients', 'directions'),
			}),
		('Nutrition Information', {
			'classes': ('',),
			'fields': ('serving_size', 'num_servings', 'calories', 'fat_cals', 'total_fat', 'saturated_fat', 'trans_fat', 'cholesterol', 'sodium', 'total_carbs', 'dietary_fiber', 'sugars', 'protein', 'vit_a', 'vit_c', 'calcium', 'iron')
			}),
		('Notes', {
			'classes': ('wide',),
			'fields': ('notes',),
			}),
		)
	filter_horizontal = ('aliases',)

admin.site.register(Recipe, RecipeAdmin)


class URLAliasAdmin(admin.ModelAdmin):
	fields = ('urlname',)

admin.site.register(URLAlias, URLAliasAdmin)


class PDFAdmin(admin.ModelAdmin):
	list_display = ('title', 'posting_time',)
	list_filter = ('posting_time',)
	search_fields = ('title',)
	fieldsets = (
		('PDF info', {
			'fields' : ('active', 'posting_time', 'display_time', 'title', 'description',),
		}),
		('PDF file', {
			'classes': ('wide',),
			'fields': ('pdf', 'thumbnail'),
		})
	)

admin.site.register(PDF, PDFAdmin)


class MediaResultAdmin(admin.ModelAdmin):
	list_display = ('headline', 'sort_order', 'posting_time')
	list_filter = ('posting_time',)
	search_fields = ('headline',)
	fieldsets = (
		('Media Result', {
			'fields' : ('active', 'posting_time', 'display_time', 'urlname', 'aliases', 'keywords', 'meta_description'),
		}),
		('Content', {
			'classes': ('wide',),
			'fields': ('headline', 'byline', 'byline_link', 'blurb', 'content',),
		}),
		('Image', {
			'classes': ('wide',),
			'fields': ('image',),
		}),
		('Marketing Banner', {
			'classes': ('wide',),
			'fields': ('marketing_banner',),
		})
	)
	filter_horizontal = ('aliases',)

admin.site.register(MediaResult, MediaResultAdmin)


class TrendingTopicAdmin(admin.ModelAdmin):
	list_display = ('headline', 'sort_order')
	list_filter = ('sort_order',)
	search_fields = ('headline',)
	fieldsets = (
		('Trending Topic', {
			'fields' : ('active', 'headline', 'content', 'sort_order'),
		}),
		('Experts', {
			'classes': ('wide',),
			'fields': ('experts',),
		}),
		('Image', {
			'classes': ('wide',),
			'fields': ('image',),
		})
	)
	filter_horizontal = ('experts',)

admin.site.register(TrendingTopic, TrendingTopicAdmin)

