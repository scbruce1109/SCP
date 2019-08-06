import os
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.http import Http404, HttpResponse, HttpResponseRedirect

from analytics.mixins import ObjectViewedMixin
from carts.models import Cart

from .models import Product, ProductManager, ProductFile



class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        return Product.objects.all()


class ProductDetailSlugView(ObjectViewedMixin, DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        #instance = get_object_or_404(Product, slug=slug, active=True)
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found...")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug, active=True)
            instance = qs.first()
        except:
            raise Http404('uasmffmfmfmmfm!!')
        # object_viewed_signal.send(instance.__class__, instance=instance, request=request)
        return instance


class UserProductHistoryView(LoginRequiredMixin, ListView):
    template_name = "products/user-history.html"
    # template_name = "products/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    # def get_context_data(self, *args, **kwargs):
    #     context = super(ProductListView, self).get_context_data(*args, **kwargs)
    #     print(context)
    #     return context

    def get_queryset(self, *args, **kwargs):
        request = self.request
        views = request.user.objectviewed_set.by_model(Product, model_queryset=False) #all().filter(content_type='prodcut')
        # viewed_ids = [x.object_id for x in views]
        # return Product.objects.filter(pk__in=viewed_ids)
        return views




from wsgiref.util import FileWrapper # used to be in django
from django.conf import settings
from mimetypes import guess_type
from orders.models import ProductPurchase

class ProductDownloadView(View):
    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        pk = kwargs.get('pk')
        downloads_qs = ProductFile.objects.filter(pk=pk, product__slug=slug)
        if downloads_qs.count() != 1:
            raise Http404("download not found")
        download_obj = downloads_qs.first()

        #### permission checks
        can_download = False
        user_ready = True
        if download_obj.user_required:
            if not request.user.is_authenticated():
                user_ready = False
        pruchased_products = Product.objects.none()
        if download_obj.free:
            can_download = True
        else:
            # not free
            purchased_products = ProductPurchase.objects.products_by_request(request)
            if download_obj.product in purchased_products:
                can_download = True

        if not can_download or not user_ready:
            messages.error(request, "You do not have access to downlaod this item")
            return redirect(download_obj.get_default_url())


        if settings.STATIC_MODE == 'local':
            ############# for local protected folder
            file_root = settings.PROTECTED_ROOT
            filepath = download_obj.file.path
            final_filepath = os.path.join(file_root, filepath) # where the file is store
            print(final_filepath)
            with open(final_filepath, 'rb') as f:
                wrapper = FileWrapper(f)
                mimetype = 'application/force-download'
                guessed_mimetype = guess_type(filepath)[0]
                if guessed_mimetype:
                    mimetype = guessed_mimetype
                response = HttpResponse(wrapper, content_type=mimetype)
                response['Content-Disposition'] = "attachment;filename=%s" %(download_obj.name)
                response["X-SendFile"] = str(download_obj.name)
                print(download_obj.name)
                return response




        elif settings.STATIC_MODE == 'aws':
            #################### AWS download link
            aws_filepath = download_obj.generate_download_url()
            print(aws_filepath)
            return HttpResponseRedirect(aws_filepath)
