import datetime
from haystack import indexes
from smgsite.doctors.models import Doctor, Specialty


class DoctorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.MultiValueField(document=True)
    services = indexes.MultiValueField(faceted=True)
    hospitals = indexes.MultiValueField(faceted=True)
    languages = indexes.MultiValueField(faceted=True)
    locations = indexes.MultiValueField(faceted=True)
    gender = indexes.MultiValueField(model_attr='gender',faceted=True)
    accepting = indexes.MultiValueField(model_attr='accepting_flag',faceted=True)
    last_name = indexes.CharField(model_attr='last_name') # for sort order
    
    suggestions = indexes.FacetCharField()

    using = None

    def get_model(self):
        return Doctor

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        self.using = using
        return self.get_model().objects.all()

    def prepare(self, obj):
        prepared_data = super(DoctorIndex, self).prepare(obj)
        prepared_data['suggestions'] = ', '.join(prepared_data['text'])
        return prepared_data

    def prepare_services(self, obj):
        return [(i.name) for i in obj.services.all()] + [obj.title_service.name]

    def prepare_hospitals(self, obj):
        return [(i.hospital) for i in obj.hospitals.all()]

    def prepare_text(self, obj):
        if self.using == 'flyover':
            values = [obj.first_name, obj.last_name, obj.title_service.name]
        else:
            values = [i.specialty for i in obj.specialties.all()]
            values.extend([i.name for i in obj.services.all()])
            values.append(obj.title_service.name)
            values.append(obj.first_name)
            values.append(obj.last_name)
            values.append(obj.touch)
            values.extend([location.location.address + " " + location.location.address2 + " " + 
                location.location.city + " " + location.location.state + " " + 
                location.location.display_name for location in obj.location_set.all()])
        
        return values

    def prepare_languages(self, obj):
        return [(i.language) for i in obj.languages.all()]

    def prepare_locations(self, obj):
        return [(i.location.city) for i in obj.location_set.all()]

    def prepare_gender(self, obj):
        return obj.get_gender_display()

    def prepare_accepting(self, obj):
        return obj.get_accepting_flag_display()

    def prepare_last_name(self, obj):
        return obj.last_name.replace('-', '')

        
class SpecialtyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    specialty = indexes.CharField(model_attr="specialty")

    def get_model(self):
        return Specialty

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

