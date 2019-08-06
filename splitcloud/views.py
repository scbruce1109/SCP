from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, get_user_model


def home_page(request):
    context = {
        "title":"Split Cloud Productions",
        "content":"Homepage",
    }
    if request.user.is_authenticated:
        context['premium_content'] = 'squuuirrrrrt'
    return render(request, "home-page.html", context)
