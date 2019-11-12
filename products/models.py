import random
import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.db.models import Q
from django.urls import reverse
from splitcloud.utils import unique_slug_generator, get_filename

from splitcloud.AWS.utils import ProtectedS3Storage
from splitcloud.AWS.download.utils import AWSDownload

# Create your models here.
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
    return "products/{dir_name}/{final_filename}".format(
            dir_name=dir_name,
            final_filename=final_filename
            )






class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True)

    def search(self, query):
        lookups =   (Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(price__icontains=query) |
                    Q(tag__title__icontains=query)
                    )
        return self.filter(lookups).distinct()

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id) # Product.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        else:
            return None

    def search(self, query):
        return self.get_queryset().active().search(query)

class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20, default=99.99)
    image = models.ImageField(upload_to=upload_media_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_digital = models.BooleanField(default=False) # User Library
    is_beat = models.BooleanField()



    objects = ProductManager()

    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse("products:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title

    def get_downloads(self):
        qs = self.productfile_set.all()
        return qs

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)

def upload_product_file_loc(instance, filename):
    slug = instance.product.slug
    id_ = instance.id
    if id_ is None:
        Klass = instance.__class__
        qs = Klass.objects.all().order_by('-pk')
        if qs.exists():
            id_ = qs.first().id + 1
        else:
            id = 0
    if not slug:
        slug = unique_slug_generator(instance.product)
    location = "product/{slug}/{id}/".format(slug=slug, id=id_)
    return location + filename # path/to/filename.mp3




class ProductFile(models.Model):
    product         = models.ForeignKey(Product, on_delete=models.PROTECT)
    name            = models.CharField(max_length=120, null=True, blank=True)
    file            = models.FileField(
                        upload_to=upload_product_file_loc,
                        storage=FileSystemStorage(location=settings.PROTECTED_ROOT),  ### use location=settings.PROTECTED_ROOT for local
                        )
    free            = models.BooleanField(default=False) # purchase required
    user_required   = models.BooleanField(default=False) # user doesn't matter

    def __str__(self):
        return str(self.file.name)

    @property
    def display_name(self):
        og_name = get_filename(self.file.name)
        if self.name:
            return self.name
        return og_name

    def get_default_url(self):
        return self.product.get_absolute_url()



    def generate_download_url(self):
        bucket = getattr(settings, 'AWS_STORAGE_BUCKET_NAME')
        region = getattr(settings, 'S3DIRECT_REGION')
        access_key = getattr(settings, 'AWS_ACCESS_KEY_ID')
        secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY')
        if not secret_key or not access_key or not bucket or not region:
            print('guhhh')
            return "/product-not-found/"
        PROTECTED_DIR_NAME = getattr(settings, 'PROTECTED_DIR_NAME', 'protected')
        path = "{base}/{file_path}".format(base=PROTECTED_DIR_NAME, file_path=str(self.file))
        print(path)
        aws_dl_object =  AWSDownload(access_key, secret_key, bucket, region)
        file_url = aws_dl_object.generate_url(path, new_filename=self.display_name)
        return file_url


    def get_download_url(self):
        return reverse("products:download", kwargs={"slug": self.product.slug, "pk": self.pk})



############## Beat Stuff

class BeatQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

class BeatManager(models.Manager):
    def get_queryset(self):
        return BeatQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

class Beat(models.Model):
    title = models.CharField(max_length=120)
    filename = models.CharField(max_length=120)
    bpm = models.CharField(max_length=5, null=True, blank=True)
    active = models.BooleanField(default=True)
    cover_art = models.ImageField(upload_to=upload_media_path, null=True, blank=True)
    audio_file = models.FileField(upload_to=upload_media_path, null=True, blank=True)
    slug = models.SlugField(blank=True, unique=True)
    standard = models.ForeignKey(Product, blank=True, null=True, related_name='standard_lease', on_delete=models.PROTECT)
    trackout = models.ForeignKey(Product, blank=True, null=True, related_name='trackout_lease', on_delete=models.PROTECT)
    unlimited = models.ForeignKey(Product, blank=True, null=True, related_name='unlimited_lease', on_delete=models.PROTECT)

    objects = BeatManager()

    def __str__(self):
        return self.title

    def get_mp3_url(self):
        return 'media/' + self.filename

    def has_audio(self):
        if self.audio_file:
            return True
        return False


def beat_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.has_audio():
        instance.active = False
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(beat_pre_save_receiver, sender=Beat)
