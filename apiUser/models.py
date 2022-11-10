from django.db import models
from utils import converter


class Content(models.Model):
    """
        title: 제목
        content: 내용
        author: 작성자
        like_count: 좋아요 카운트
        pub_date: 배포일
    """

    uid = models.TextField()
    dir = models.TextField(blank=True)
    key = models.TextField()

    def __str__(self):
        return converter.dir2path(self.uid, self.dir, self.key)
