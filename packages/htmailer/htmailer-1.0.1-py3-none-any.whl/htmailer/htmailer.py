from django.core.mail import EmailMultiAlternatives
from .resolver import TemplateResolver

class Htmessage(EmailMultiAlternatives):
	"""
	Htmessage is an extension of django's official EmailMessage.

	It is adapted to work with django templating engine or any templating engine adapted to work with django.
	"""

	def __init__(self, subject='', from_email=None, to=None, bcc=None, 
		connection=None, attachments=None, headers=None, cc=None, 
		reply_to=None, Resolver=None):
		"""
		Call the super class's constructor to gain access to parent's methods and fields.

		The resolver used is injected into the constructor but defaults to TemplateResolver.
		"""
		super(Htmessage, self).__init__(subject=subject, from_email=from_email, to=to, bcc=bcc,
			connection=connection, attachments=attachments, headers=headers, cc=cc, reply_to=reply_to)
		self._txt_message = None
		self._html_message = None
		self._resolver = Resolver or TemplateResolver
		self.body = ''
	
	def get_txt_msg(self):
		return self._txt_message

	def get_html_msg(self):
		return self._html_message

	def txt_template(self, template, context={}):
		self._txt_message = self._resolver.render(path=template, context=context)
		self.body = self._txt_message
		return self

	def html_template(self, template, context={}):
		self._html_message = self._resolver.render(path=template, context=context)
		self.attach_alternative(self._html_message, "text/html")
		return self




