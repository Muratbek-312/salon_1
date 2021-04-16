from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import UpdateView, ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from django.views.generic.base import View

from django.http import HttpResponse
from service.models import Category
from service.views import IsAdminMixin
from .models import MasterProfile, CustomerProfile, Rating
from .forms import RatingForm, MasterProfileForm, CommentForm

User = get_user_model()


class MasterProfileListView(ListView):
    model = MasterProfile
    template_name = 'profile/master_list.html'
    context_object_name = 'masterprofiles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class MasterProfileDetailView(FormMixin, DetailView):
    model = MasterProfile
    template_name = 'profile/master_details.html'
    context_object_name = 'get_masterprofiles'
    form_class = CommentForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["star_form"] = RatingForm()
        return context


class MasterProfileEditView(IsAdminMixin, View):
    def get(self, request, pk):
        master = get_object_or_404(MasterProfile, pk=pk)
        form = MasterProfileForm(instance=master)
        return render(request, 'profile/master_edit.html', locals())

    def post(self, requset, pk):
        master = get_object_or_404(MasterProfile, pk=pk)
        form = MasterProfileForm(instance=master, data=requset.POST)
        if form.is_valid():
            master = form.save()
        return redirect(master.get_absolute_url())


class CustomerProfileListView(ListView):
    model = CustomerProfile


class CustomerProfileDetailView(DetailView):
    model = CustomerProfile


class CustomerProfileUpdateView(UpdateView):
    model = CustomerProfile


class AddStarRating(View):
    """Добавление рейтинга"""
    def get_client_user(self, request):
        user_name = request.user.nik_name
        if user_name:
            user = user_name.split(',')[0]
        else:
            user = request.user.nik_name
        return user

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                user=self.get_client_user(request),
                master_id=int(request.POST.get("masterprofile")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class AddComment(View):
    """Коменнтарий"""
    def post(self, request, pk):
        masterprofile = get_object_or_404(MasterProfile, id=pk)
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.master = masterprofile
                comment.user = request.user.nik_name
                comment.save()
        else:
            form = CommentForm()
        return render(request, 'profile/master_details.html', {'masterprofile': masterprofile, "form": form})

