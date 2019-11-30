from django.contrib import admin

# Register your models here.
from .models import Cart, DiscountCode

admin.site.register(Cart)

admin.site.register(DiscountCode)
