from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, get_user_model
from .forms import ContactForm

from products.models import Beat
from carts.models import Cart

from transactional.utils import SendInBlue

from django.core.mail import send_mail
from django.template.loader import get_template


def home_page(request):
    context = {
        "title":"Split Cloud Productions",
        "content":"Homepage",
    }
    if request.user.is_authenticated:
        context['premium_content'] = 'squuuirrrrrt'
    return render(request, "home-page.html", context)


def about_page(request):
    context = {
        "title":"Split Cloud Productions",
        "content":"About",
    }
    return render(request, "about-page.html", context)


def services_page(request):
    context = {
        "title":"Split Cloud Productions",
        "content":"Services",
    }
    return render(request, "services-page.html", context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title":"Contact",
        "content":"",
        "form": contact_form,
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        subject = contact_form.cleaned_data.get('subject', '')
        sender_name = contact_form.cleaned_data.get('name')
        sender_email = contact_form.cleaned_data.get('email')
        message = contact_form.cleaned_data.get('content', '')
        send_context = {'message': message}

        txt_ = get_template("contact/emails/contact_message.txt").render(send_context)
        html_ = get_template("contact/emails/contact_message.html").render(send_context)
        # from_email = settings.DEFAULT_FROM_EMAIL
        sendinblue = SendInBlue()
        sent_email = sendinblue.send_contact_email(sender_name, sender_email, html_, txt_, subject)
        # sent_mail = send_mail(
        #             subject,
        #             txt_,
        #             from_email,
        #             recipient_list,
        #             html_message=html_,
        #             fail_silently=False,
        #             )
        # if sent_mail:
        #     print('email sent beeeeetch')
        print(sent_email.content)
        if request.is_ajax():
            return JsonResponse({"message": "thank you"})

    if contact_form.errors:
        print(contact_form.errors)
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')
    # if request.method == "POST":
    #     print(request.POST)
    #     print(request.POST.get('fullname'))
    return render(request, "contact-page.html", context)



    # context = {
    #     "title":"Split Cloud Productions",
    #     "content":"Contact",
    # }
    # return render(request, "contact-page.html", context)


def new_home(request):
    context = {
        "title":"Split Cloud Productions",
        "content":"Hiii",
    }
    # if request.user.is_authenticated:
    #     context['premium_content'] = 'squuuirrrrrt'
    return render(request, "new_home.html", context)


class BeatStoreView(ListView):
    queryset = Beat.objects.all()
    template_name = "new_home.html"

    def get_context_data(self, *args, **kwargs):
        context = super(BeatStoreView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        print(context)
        return context
