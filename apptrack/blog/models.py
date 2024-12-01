from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = CKEditor5Field()
    summary = models.TextField()
    published = models.DateTimeField()

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.title
