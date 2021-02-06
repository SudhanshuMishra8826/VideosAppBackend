from django.db import models
from django.conf import settings
from django.utils import timezone


class Videos(models.Model):
  video_id = models.AutoField(primary_key=True)
  name = models.CharField(max_length=200)
  description = models.TextField(max_length=10000)  
  url = models.CharField(max_length=200)
  thumbnail = models.CharField(max_length=200)
  lang = models.CharField(max_length=200)
  upload_date = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return self.name


class VideosTopics(models.Model):
  topic_id = models.AutoField(primary_key=True)
  video_id = models.ManyToManyField(Videos)

  def __str__(self):
    return str(self.topic_id)