from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save

from .utils import Mailchimp

# Create your models here.
class MarketingPreference(models.Model):
    user                        = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    subscribed                  = models.BooleanField(default=True)
    mailchimp_subscribed        = models.NullBooleanField(blank=True)
    mailchimp_msg               = models.TextField(null=True, blank=True)
    timestamp                   = models.DateTimeField(auto_now_add=True)
    updated                      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


def marketing_pref_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        print(instance.user.email)
        status_code, response_data = Mailchimp().subscribe(instance.user.email)
        print(status_code, response_data)

post_save.connect(marketing_pref_create_receiver, sender=MarketingPreference)


def marketing_pref_update_receiver(sender, instance, *args, **kwargs):
    print(instance.user.email)
    if instance.subscribed != instance.mailchimp_subscribed:
        if instance.subscribed:
            print('squuueeeert')
            status_code, response_data = Mailchimp().subscribe(instance.user.email)
        else:
            status_code, response_data = Mailchimp().unsubscribe(instance.user.email)
        if response_data['status'] == 'subscribed':
            instance.subscribed = True
            instance.mailchimp_subscribed = True
            instance.mailchimp_msg = response_data
        else:
            instance.subscribed = False
            instance.mailchimp_subscribed = False
            instance.mailchimp_msg = response_data

pre_save.connect(marketing_pref_update_receiver, sender=MarketingPreference)



def make_marketing_pref_receiver(sender, instance, created, *args, **kwargs):
    '''
    User model
    '''
    if created:
        MarketingPreference.objects.get_or_create(user=instance)

post_save.connect(make_marketing_pref_receiver, sender=settings.AUTH_USER_MODEL)


class CampaignChoices(models.Model):
    campaign_type = models.CharField(max_length=150)

    def __str__(self):
        return self.campaign_type



class Subscriber(models.Model):
    name                        = models.CharField(max_length=150)
    email                       = models.EmailField(max_length=255, unique=True)
    campaign                    = models.ManyToManyField(CampaignChoices)
    referring_link              = models.CharField(max_length=255, blank=True, null=True)
    subscribed                  = models.BooleanField(default=True)
    mailchimp_subscribed        = models.NullBooleanField(blank=True)
    mailchimp_msg               = models.TextField(null=True, blank=True)
    timestamp                   = models.DateTimeField(auto_now=True)
    update                      = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


def subscriber_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        print(instance.email)
        status_code, response_data = Mailchimp().subscribe(instance.email)
        print(status_code, response_data)

post_save.connect(subscriber_create_receiver, sender=Subscriber)


def subscriber_update_receiver(sender, instance, *args, **kwargs):
    print(instance.email)
    if instance.subscribed != instance.mailchimp_subscribed:
        if instance.subscribed:
            print('squuueeeert')
            status_code, response_data = Mailchimp().subscribe(instance.email)
        else:
            status_code, response_data = Mailchimp().unsubscribe(instance.email)
        if response_data['status'] == 'subscribed':
            instance.subscribed = True
            instance.mailchimp_subscribed = True
            instance.mailchimp_msg = response_data
        else:
            instance.subscribed = False
            instance.mailchimp_subscribed = False
            instance.mailchimp_msg = response_data

pre_save.connect(subscriber_update_receiver, sender=Subscriber)
