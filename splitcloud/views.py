from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth import authenticate, login, get_user_model

from beatstore.models import Beat


def home_page(request):
    context = {
        "title":"Split Cloud Productions",
        "content":"Homepage",
    }
    if request.user.is_authenticated:
        context['premium_content'] = 'squuuirrrrrt'
    return render(request, "home-page.html", context)


def new_home(request):
    context = {
        "title":"Split Cloud Productions",
        "content":"Hiii",
    }
    # if request.user.is_authenticated:
    #     context['premium_content'] = 'squuuirrrrrt'
    return render(request, "new_home.html", context)


class NewHomeList(ListView):
    queryset = Beat.objects.all()
    template_name = "new_home.html"

    def get_context_data(self, *args, **kwargs):
        context = super(NewHomeList, self).get_context_data(*args, **kwargs)
        print(context)
        return context
