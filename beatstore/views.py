from django.shortcuts import render
from django.views.generic import ListView, DetailView
# Create your views here.
from .models import Beat

class BeatListView(ListView):
    queryset = Beat.objects.all()
    template_name = "beatstore/beatstore.html"

    def get_context_data(self, *args, **kwargs):
        context = super(BeatListView, self).get_context_data(*args, **kwargs)
        print(context)
        return context


# class BeatDetailSlugView(DetailView):
#     queryset = Beat.objects.all()
#     template_name = "products/detail.html"
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
#         cart_obj, new_obj = Cart.objects.new_or_get(self.request)
#         context['cart'] = cart_obj
#         return context
#
#     def get_object(self, *args, **kwargs):
#         request = self.request
#         slug = self.kwargs.get('slug')
#         #instance = get_object_or_404(Product, slug=slug, active=True)
#         try:
#             instance = Product.objects.get(slug=slug, active=True)
#         except Product.DoesNotExist:
#             raise Http404("Not found...")
#         except Product.MultipleObjectsReturned:
#             qs = Product.objects.filter(slug=slug, active=True)
#             instance = qs.first()
#         except:
#             raise Http404('uasmffmfmfmmfm!!')
#         # object_viewed_signal.send(instance.__class__, instance=instance, request=request)
#         return instance
