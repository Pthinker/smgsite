import datetime
from haystack import indexes
from smgsite.events.models import Event, Class

class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr="title")

    def get_model(self):
        return Event

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class ClassIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr="title")

    def get_model(self):
        return Class

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

