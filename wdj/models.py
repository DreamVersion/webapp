# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class WDJ(models.Model):
    package_name = models.CharField(max_length= 300)
    package_id = models.CharField(max_length= 300, primary_key= True)
    package_content = models.CharField(max_length=1024*1024)
    update_time = models.DateTimeField('update time')

    class Meta:
        verbose_name = "App"
        verbose_name_plural = "Apps"

    def __str__(self):
        return self.package_name