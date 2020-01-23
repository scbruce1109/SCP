from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, get_user_model

from products.models import Beat
from carts.models import Cart


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
    context = {
        "title":"Split Cloud Productions",
        "content":"Contact",
    }
    return render(request, "contact-page.html", context)


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
