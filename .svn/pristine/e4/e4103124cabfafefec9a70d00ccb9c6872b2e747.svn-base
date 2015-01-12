class Result(object):
	def __init__(self, items):
		self.model = items[0]
		self.key = items[1]
		self.url = items[2]
		self.name = items[3]


class ResultGroup(object):
	def __init__(self, name, more, order, results, display_name):
		self.__dict__.update(locals())
		del self.self


class SearchKey(object):	
	def __init__(self, key, url, order, display, name, body):
		self.__dict__.update(locals())
		del self.self


class Keyword(object):	
	def __init__(self, model, searchkey):
		self.__dict__.update(locals())
		del self.self
