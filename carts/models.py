from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save, m2m_changed

from products.models import Product

User = settings.AUTH_USER_MODEL




class DiscountCodeQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def by_code(self, code):
        return self.filter(code__iexact=code)


class DiscountCodeManager(models.Manager):
    def get_queryset(self):
        return DiscountCodeQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()



class DiscountCode(models.Model):
    code = models.CharField(max_length=120, blank=True)
    discount = models.DecimalField(default=0.00, max_digits=65, decimal_places=2)
    active = models.BooleanField(default=True)
    users = models.ManyToManyField(User, blank=True, null=True)

    objects = DiscountCodeManager()

    def __str__(self):
        return self.code

    def is_active(self):
        return self.active

    def can_use(self, user):
        qs = self.users.all()
        if user not in qs and self.is_active():
            return True
        else:
            return False





class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        print(user)
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)

class Cart(models.Model):
    user        = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    products    = models.ManyToManyField(Product, blank=True)
    total       = models.DecimalField(default=0.00, max_digits=65, decimal_places=2)
    subtotal    = models.DecimalField(default=0.00, max_digits=65, decimal_places=2)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    discount    = models.ForeignKey(DiscountCode, on_delete=models.PROTECT, null=True, blank=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    @property
    def is_digital(self):
        qs = self.products.all()
        new_qs = qs.filter(is_digital=False)
        if new_qs.exists():
            return False
        return True


    def has_discount(self):
        if self.discount:
            return True
        else:
            return False

    def apply_discount(self, code):
        qs = DiscountCode.objects.all().by_code(code)
        if qs.exists():
            discount_code = qs.first()
            discount = self.subtotal * discount_code.discount
            new_total = self.subtotal - discount
            self.total = new_total
            self.discount = discount_code
            self.save()
            data = {
                    'discount': discount,
                    'new_total': new_total,
                    }
            return data
        else:
            return None




def m2m_changed_cart_receiver(sender, instance, action, *args, **kwargs):
    if action == "post_add" or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(m2m_changed_cart_receiver, sender=Cart.products.through)

def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        if instance.has_discount():
            discount = instance.subtotal * instance.discount.discount
            new_total = instance.subtotal - discount
            instance.total = new_total
        else:
            instance.total = float(instance.subtotal)
    else:
        instance.total = 0

pre_save.connect(pre_save_cart_receiver, sender=Cart)
