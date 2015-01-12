from string import ascii_lowercase 

from django.conf import settings

def alpha_list_processor(request):  
    """ provide a list of all the letter in the alphabet to all templates to render alpha jump widget """
    alpha_list = list(ascii_lowercase)        
    return {'alpha_list': alpha_list}


def extra_template_data(request):
    """ extra stuff from settings for use in the template """
    data = {
        'GOOGLE_MAP_KEY': getattr(settings, 'GOOGLE_MAP_KEY', None),
        'GOOGLE_ANALYTICS_CODE': getattr(settings, 'GOOGLE_ANALYTICS_CODE', None),
    }
    return data