import datetime
from haystack import indexes
from smgsite.articles.models import Article, MediaResult, Feature, Recipe


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    headline = indexes.CharField(model_attr="headline")

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class MediaResultIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    headline = indexes.CharField(model_attr="headline")

    def get_model(self):
        return MediaResult

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class FeatureIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    headline = indexes.CharField(model_attr="headline")

    def get_model(self):
        return Feature

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class RecipeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr="title")

    def get_model(self):
        return Recipe

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

