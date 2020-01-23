from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url
from .utils import get_paypal_token, get_order_details
# Create your views here.


import stripe
STRIPE_PUB_KEY = getattr(settings, 'STRIPE_PUB_KEY', 'pk_test_NDDVONYz0ZEtqGhrmOtnDKxw')
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_HAJZxFu1o25Igf8UvjOyI2ZK")
stripe.api_key = STRIPE_SECRET_KEY

from .models import BillingProfile, Card


def payment_method_view(request):
    # if request.user.is_authenticated():
    #     billing_profile = request.user.billingprofile
    #     my_customer_id = billing_profile.customer_id
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect("/cart")

    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_

    return render(request, 'billing/payment_method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})


def payment_method_create_view(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message": "Cannot find this user"})

        token = request.POST.get("token")
        if token is not None:
            # customer = stripe.Customer.retrieve(billing_profile.customer_id)
            # card_response = customer.sources.create(source=token)
            # new_card_obj = Card.objects.add_new(billing_profile, card_response)
            new_card_obj = Card.objects.add_new(billing_profile, token)
            request.session['card_active'] = True
            print(new_card_obj) # start saving our cards
        return JsonResponse({"message": "Success! Card was added"})
    return HttpResponse("error", status_code=401)


def paypal_transaction_complete_view(request):
    if request.method == "POST" and request.is_ajax():
        order_id = request.POST.get('order_id')
        print(order_id)
        if order_id is not None:
            order_details = get_order_details(order_id)
            print(order_details)
            return JsonResponse({"message": "Success!"})
    return HttpResponse("error", status_code=401)
