from django.template.loader import get_template
from abc import abstractmethod, ABC
from django.test import TestCase

class Resolver(ABC):

	@abstractmethod
	def render():
		pass

class TemplateResolver(Resolver):
	"""This class should implement a way to set things like urls in tne mail."""
	
	@classmethod
	def render(cls, path, context={}):
		if type(context) != dict:
			raise TypeError('context must be a dictionary')
		template = get_template(template_name=path)
		return template.render(context)

class TestResolver(ABC, TestCase):
	
	TEST_MESSAGE = 'THIS IS A TEST STRING, IT DOES NOT USE THE PROVIDED PARAMS'
	
	@classmethod
	def render(cls, path, context={}):
		return cls.TEST_MESSAGE  #this must be same as TEST_MESSAGE or tests will fail

