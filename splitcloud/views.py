from django.http import HttpResponse
from django.shortcuts import render


def home_page(request):
    context = {
        "title":"Split Cloud Productions",
        "content":"Homepage",
    }
    return render(request, "home-page.html", context)
