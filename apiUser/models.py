from django.db import models
from utils import converter


class Content(models.Model):

    uid = models.CharField(max_length=64)
    dir = models.CharField(max_length=200, blank=True)
    key = models.CharField(max_length=100)

    def __str__(self):
        return converter.dir2path(self.uid, self.dir, self.key)
