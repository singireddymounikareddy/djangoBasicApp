from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings

# Create your models here.
class Post(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	title=models.CharField(max_length=120)
	image=models.ImageField(null=True,blank=True,width_field="width_field",height_field="height_field")
	width_field=models.IntegerField(default=0)
	height_field=models.IntegerField(default=0)
	content=models.TextField()
	updated=models.DateTimeField(auto_now=True,auto_now_add=False)
	timestamp=models.DateTimeField(auto_now=False,auto_now_add=True)
	def __unicode__(self):
		return self.title
	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"id":self.id})
	class Meta:
		ordering=["-timestamp","-updated"]

