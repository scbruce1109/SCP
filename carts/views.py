from django.conf import settings
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect

from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail

from addresses.forms import AddressForm
from addresses.models import Address

from billing.utils import get_paypal_token, get_order_details
from billing.models import BillingProfile
from orders.models import Order, ProductPurchase
from products.models import Product
from .models import Cart, DiscountCode
from .forms import DiscountCodeForm

from transactional.utils import SendInBlue

from django.core.mail import send_mail
from django.template.loader import get_template

import stripe
STRIPE_PUB_KEY = getattr(settings, 'STRIPE_PUB_KEY', 'pk_test_NDDVONYz0ZEtqGhrmOtnDKxw')
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_HAJZxFu1o25Igf8UvjOyI2ZK")
stripe.api_key = STRIPE_SECRET_KEY

def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
            "id": x.id,
            "url": x.get_absolute_url(),
            "name": x.name,
            "price": x.price
            }
            for x in cart_obj.products.all()]
    cart_data = {"products": products, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    return JsonResponse(cart_data)



def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    print(cart_obj.is_digital)
    return render(request, "carts/home.html", {"cart": cart_obj})

def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Product does not exist")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
        else:
            cart_obj.products.add(product_obj)
            added = True
        request.session['cart_items'] = cart_obj.products.count()
        if request.is_ajax():
            print("Ajax request")
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count()
            }
            return JsonResponse(json_data)
    return redirect("cart:home")


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    print(cart_obj.total)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect("cart:home")
    login_form = LoginForm(request=request)
    guest_form = GuestForm(request=request)
    address_form = AddressForm()
    discount_form = DiscountCodeForm()
    billing_address_id = request.session.get("billing_address_id", None)

    shipping_address_required = not cart_obj.is_digital


    shipping_address_id = request.session.get("shipping_address_id", None)


    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    has_card = False
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id or shipping_address_id:
            order_obj.save()
        has_card = billing_profile.has_card

    if cart_obj.has_discount():
        discount_amount = round(cart_obj.subtotal * cart_obj.discount.discount,2)
    else:
        discount_amount = 0

    address_active = request.session.get('address_active', False)
    card_active = request.session.get('card_active', False)

    if request.method == "POST":
        "Check that order is done"
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, crg_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid(request)
                request.session['cart_items'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_cards_inactive()
                print('wooop')
                request.session['order_id'] = order_obj.order_id
                return redirect("cart:success")
            else:
                print(crg_msg)
                print('nahhh')
                return redirect("cart:checkout")

    context = {
        "object": order_obj,
        "cart_obj": cart_obj,
        "cart_discount": cart_obj.has_discount(),
        "address_active": address_active,
        "card_active": card_active,
        "discount_amount": discount_amount,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
        "discount_form": discount_form,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
        'shipping_address_required': shipping_address_required,
    }
    return render(request, "carts/checkout.html", context)


def paypal_transaction_complete_view(request):
    if request.method == "POST" and request.is_ajax():
        cart_obj, cart_created = Cart.objects.new_or_get(request)
        order_obj = None
        if cart_created or cart_obj.products.count() == 0:
            return redirect("cart:home")

        order_id = request.POST.get('order_id')
        if order_id is not None:
            order_details = get_order_details(order_id)
            id = order_details.get('id')
            status = order_details.get('status')

            billing_profile, billing_profile_created = BillingProfile.objects.paypal_new_or_get(order_details)

            if billing_profile is not None:
                order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)

                if status == 'COMPLETED':
                    order_obj.mark_paid(request)
                    request.session['cart_items'] = 0
                    del request.session['cart_id']
                    return JsonResponse({"message": "Success!"})

                elif id is not None:
                    order_obj.order_id = id
                    order_obj.save()
                    return JsonResponse({"message": "Error"})

                else:
                    print('something happend')


            # print(status)
            # print(email)
            # print(first_name)


    return HttpResponse("error", status_code=401)



def checkout_done_view(request):
    if request.session['order_id']:
        #### check this part, add .get below
        id = request.session['order_id']
        qs = Order.objects.all().by_id(id)
        order_obj = qs.first()
        email = order_obj.billing_profile.email
        cart_obj = order_obj.cart
        product_list = cart_obj.products.all()
        context = {
            "product_list": product_list,
        }
        print('order successful')

        txt_ = get_template("transactional/emails/order.txt").render(context)
        html_ = get_template("transactional/emails/order.html").render(context)
        subject = 'Your order'
        # from_email = settings.DEFAULT_FROM_EMAIL
        recipient = email
        sendinblue = SendInBlue()
        sent_email = sendinblue.send_transactional_email(email, html_, txt_, subject)
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
        print(sent_email)
        logout(request)

        return render(request, "carts/checkout-done.html", context)
    else:
        return redirect("cart:checkout")



def discount_code_apply_view(request):
    if request.method == "POST" and request.is_ajax():
        response_data = {}
        code = request.POST.get('discount_code')
        cart_obj, created = Cart.objects.new_or_get(request)
        data = cart_obj.apply_discount(code)
        if data is not None:
            response_data['success'] = True
            response_data['message'] = 'Success! Discount code applied'
            response_data['new_total'] = round(data['new_total'],2)
            response_data['discount_amount'] = round(data['discount'],2)
        else:
            response_data['message'] = 'Discount code is not valid or has expired'
        return JsonResponse(response_data)
    return redirect("cart:checkout")
