from urllib import quote_plus
from django import template

regiser=template.Library()

@regiser.filter
def urlify(value):
	return quote_plus(value)
