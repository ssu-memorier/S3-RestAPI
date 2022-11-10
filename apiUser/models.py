from django.db import models
from utils import converter


class Content(models.Model):

    uid = models.TextField()
    dir = models.TextField(blank=True)
    key = models.TextField()

    def __str__(self):
        return converter.dir2path(self.uid, self.dir, self.key)
