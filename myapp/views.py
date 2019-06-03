from django.contrib.auth import authenticate, login
from django.http import request, HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.base import View
from django.shortcuts import render
from .forms import LoginForm, RegisterForm
from .models import User, Post, Replies


# def RegisterView(request):
#     form_class = RegisterForm()
#     return render(request, '')


# def IndexView(request):
#     login_form= LoginForm()
#     register_form = RegisterForm()
#     # template_name = 'myapp/login.html'
#     return render(request, 'myapp/index.html', {'login_form': login_form, 'register_form': register_form})


def RegisterView(request):
    form = RegisterForm(request.POST)
    login_form = LoginForm()
    register_form = RegisterForm()
    if request.method == 'POST':
        if form.is_valid():
            address = form.cleaned_data['address']
            lastname = form.cleaned_data['last_name']
            firstname = form.cleaned_data['first_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User(first_name=firstname, last_name=lastname, email=email, address=address, password=password, username=username)
            user.set_password(password)
            user.save()
            if user is not None:
                return render(request, 'myapp/index.html', {'msg': "Successfully Registered", 'login_form': login_form})
            else:
                return render(request, {'msg': "Couldn't register"})


def LoginView(request):
    form = LoginForm(request.POST)
    register_form = RegisterForm()
    if request.method == 'POST':
        # return HttpResponse("aaa")

        if form.is_valid():

            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home/')

def HomeView(request):
    if request.method == 'GET':
        return render(request, 'myapp/home.html')


def MainpageView(request):
    # login_form= LoginForm()
    # register_form = RegisterForm()
    if request.method == 'GET':
        return render(request, 'myapp/index.html', {'login_form': LoginForm(), 'register_form': RegisterForm()})


class PostList(ListView):
    model = Post
    template_name = 'myapp/post_list.html'


class PostDetail(DetailView):
    model = Post
    template_name = 'myapp/post_detail.html'


class PostCreate(CreateView):
    model = Post
    fields = ['title', 'text', 'created_date', 'publish_date']
    # template_name = 'myapp/post_new.html'
    success_url = reverse_lazy('post_list')


class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'myapp/post_edit.html'
    success_url = reverse_lazy('post_list')


class PostDelete(DeleteView):
    model = Post
    template_name = 'myapp/post_delete.html'
    success_url = reverse_lazy('post_list')


class ReplyList(ListView):
    template_name = 'myapp/reply_list.html'
    model = Replies


class ReplyDetail(DetailView):
    model = Replies
    template_name = 'myapp/reply_detail.html'


class ReplyCreate(CreateView):
    model = Post
    fields = ['post', 'text', 'created_date']
    template_name = 'myapp/reply_new.html'
    success_url = reverse_lazy('post_list')


class ReplyUpdate(UpdateView):
    model = Post
    fields = ['post', 'text']
    template_name = 'myapp/reply_edit.html'
    success_url = reverse_lazy('post_list')


class ReplyDelete(DeleteView):
    model = Post
    template_name = 'myapp/reply_delete.html'
    success_url = reverse_lazy('post_list')





