from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, View

from .forms import MarketingPreferenceForm
from .mixins import CsrfExemptMixin
from .models import MarketingPreference
from .utils import Mailchimp

MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)

class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferenceForm
    template_name = 'base/forms.html'
    success_url = '/settings/email/'
    success_message = "Your email preferences have been updated. Thanks bitch"

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect("/login/?next=/settings/email/")
        return super(MarketingPreferenceUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Email Preference'
        return context

    def get_object(self):
        user = self.request.user

        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj

# "root":
# "type": "unsubscribe"
# "fired_at": "2019-05-31 19:45:21"
# "data":
# "action": "unsub"
# "reason": "manual"
# "id": "2b7483f952"
# "email": "hey@hi.com"
# "email_type": "html"
# "ip_opt": "164.51.130.150"
# "web_id": "21665713"
# "merges":
# "EMAIL": "hey@hi.com"
# "FNAME": ""
# "LNAME": ""
# "ADDRESS": ""
# "PHONE": ""
# "BIRTHDAY": ""
# "list_id": "4b77bf728d"


class MailchimpWebhookView(View):
    # def get(self, request, *args, **kwargs):
    #     return HttpResponse("Thank you", status=200)

    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            hook_type = data.get("type")
            email = data.get('data[email]')
            response_status, response = Mailchimp().check_subscription_status(email)
            sub_status = response['status']
            is_subbed = None
            mailchimp_subbed = None
            if sub_status == "subscribed":
                is_subbed, mailchimp_subbed = (True, True)
            if sub_status == "unsubscribed":
                is_subbed, mailchimp_subbed = (False, False)
            if is_subbed and mailchimp_subbed:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists():
                    qs.update(
                            subscribed=is_subbed,
                            mailchimp_subscribed=mailchimp_subbed,
                            mailchimp_msg=str(data)
                            )
        return HttpResponse("Thank you", status=200)
