from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextUploadingField()
    summary = models.TextField()
    published = models.DateTimeField()

    class Meta:
        ordering = ["-published"]

    def __str__(self):
        return self.title
