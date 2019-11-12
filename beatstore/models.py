import os

from django.db import models
from django.db.models.signals import pre_save

from splitcloud.utils import unique_slug_generator
from products.models import Product

def get_filename_ext(filename):
    base_name = os.path.basename(filename)
    name, ext = os.path.splitext(base_name)
    name = name.strip().replace(' ', '_')
    return name, ext

def upload_media_path(instance, filename):
    print(instance)
    print(filename)
    dir_name = instance.title.strip().replace(' ', '_')
    name, ext = get_filename_ext(filename)
    final_filename = '{name}{ext}'.format(name=name, ext=ext)
    return "beats/{dir_name}/{final_filename}".format(
            dir_name=dir_name,
            final_filename=final_filename
            )


# class BeatQuerySet(models.query.QuerySet):
#     def active(self):
#         return self.filter(active=True)
#
# class BeatManager(models.Manager):
#     def get_queryset(self):
#         return BeatQuerySet(self.model, using=self._db)
#
#     def all(self):
#         return self.get_queryset().active()
#
# class Beat(models.Model):
#     title = models.CharField(max_length=120)
#     filename = models.CharField(max_length=120)
#     bpm = models.CharField(max_length=5, null=True, blank=True)
#     active = models.BooleanField(default=True)
#     cover_art = models.ImageField(upload_to=upload_media_path, null=True, blank=True)
#     audio_file = models.FileField(upload_to=upload_media_path, null=True, blank=True)
#     slug = models.SlugField(blank=True, unique=True)
#     # standard = models.ForeignKey(Product, blank=True, null=True, related_name='standard_lease', on_delete=models.PROTECT)
#     # trackout = models.ForeignKey(Product, blank=True, null=True, related_name='trackout_lease', on_delete=models.PROTECT)
#     # unlimited = models.ForeignKey(Product, blank=True, null=True, related_name='unlimited_lease', on_delete=models.PROTECT)
#
#     objects = BeatManager()
#
#     def __str__(self):
#         return self.title
#
#     def get_mp3_url(self):
#         return 'media/' + self.filename
#
#     def has_audio(self):
#         if self.audio_file:
#             return True
#         return False
#
#
# def beat_pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.has_audio():
#         instance.active = False
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
#
# pre_save.connect(beat_pre_save_receiver, sender=Beat)
