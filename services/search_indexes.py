from haystack import indexes
from smgsite.services.models import Service

from bs4 import BeautifulSoup
import HTMLParser

def clean_content(content):
    soup= BeautifulSoup(content)
    content = soup.text.strip()
    h = HTMLParser.HTMLParser()
    return h.unescape(content)

class ServiceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    name = indexes.CharField(model_attr='name')
    using = None

    def get_model(self):
        return Service

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        self.using = using
        return self.get_model().objects.all()

    def prepare_text(self, obj):
        if self.using == 'flyover':
            value = obj.name
        else:
            arr = [obj.name, clean_content(obj.description_short), clean_content(obj.content), obj.offerings, 
                    clean_content(obj.learn_more), obj.patient_tools]
            for location in obj.location_set.all():
                loc_arr = [location.location.address, location.location.address2, location.location.city, 
                        location.location.state, location.location.display_name]
                arr.append(" ".join(loc_arr))
            value = " ".join(arr)

        return value

