from django.contrib import admin

# Register your models here.
from .models import MarketingPreference, Subscriber, CampaignChoices

class MarketingPreferenceAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'subscribed', 'updated']
    readonly_fields = ['mailchimp_subscribed','mailchimp_msg', 'timestamp', 'updated']
    class Meta:
        model = MarketingPreference
        fields = [
                    'users',
                    'subscribed',
                    'mailchimp_msg',
                    'mailchimp_subscribed',
                    'timestamp',
                    'updated'
                ]

admin.site.register(MarketingPreference, MarketingPreferenceAdmin)

admin.site.register(Subscriber)

admin.site.register(CampaignChoices)
