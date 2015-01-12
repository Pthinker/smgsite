import datetime
from haystack import indexes
from smgsite.healthday.models import Article

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    headline = indexes.CharField(model_attr="headline")

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

