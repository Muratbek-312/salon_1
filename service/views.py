from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.base import View
from django.http import Http404
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy

from .models import Category, Service, ServiceImage
from .forms import CreateServiceForm, ImagesFormSet


class IndexView(ListView):
    model = Category
    template_name = 'index.html'
    context_object_name = 'categories'


class CategoryView(ListView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'categories'


class ServiceListView(ListView):
    model = Service
    template_name = 'service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('category_slug')
        if not Category.objects.filter(slug=category_slug).exists():
            raise Http404('Нет такой категории')
        queryset = queryset.filter(categories_id=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ServiceDetailsView(DetailView):
    model = Service
    template_name = 'service_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser)


class ServiceCreateView(IsAdminMixin, View):
    def get(self, request):
        form = CreateServiceForm()
        formset = ImagesFormSet(queryset=ServiceImage.objects.none())
        return render(request, 'service_create.html', locals())

    def post(self, request):
        form = CreateServiceForm(request.POST, request.FILES)
        formset = ImagesFormSet(request.POST,
                                request.FILES,
                                queryset=ServiceImage.objects.none())
        if form.is_valid() and formset.is_valid():
            product = form.save()
            for form in formset.cleaned_data:
                image = form.get('image')
                print(image)
                if image is not None:
                    pic = ServiceImage(product=product, image=image)
                    pic.save()
                    print(image)
            return redirect(product.get_absolute_url())
        print(form.errors, formset.errors)


class ServiceEditView(IsAdminMixin, View):
    def get(self, request, pk):
        service = get_object_or_404(Service, pk=pk)
        form = CreateServiceForm(instance=service)
        formset = ImagesFormSet(queryset=service.images.all())
        return render(request, 'service_edit.html', locals())

    def post(self, requset, pk):
        service = get_object_or_404(Service, pk=pk)
        form = CreateServiceForm(instance=service, data=requset.POST)
        formset = ImagesFormSet(requset.POST, requset.FILES, queryset=service.images.all())
        if form.is_valid() and formset.is_valid():
            service = form.save()
            for form in formset.cleaned_data:
                image = form.get('image')
                if image is not None and not ServiceImage.objects.filter(service=service, image=image).exists():
                    pic = ServiceImage(service=service, image=image)
                    pic.save()
            for form in formset.deleted_forms:
                image = form.cleaned_data.get('id')
                if image is not None:
                    image.delete()

            return redirect(service.get_absolute_url())


class ServiceDeleteView(IsAdminMixin, DeleteView):
    model = Service
    template_name = 'service_delete.html'
    success_url = reverse_lazy('index-page')



