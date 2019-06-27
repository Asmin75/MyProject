from itertools import count

from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import request, HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.base import View
from django.shortcuts import render
from .forms import LoginForm, RegisterForm, PostRateForm, ReplyPostForm, QuestionRateForm
from .models import User, Post, Replies, Postratings, Questions, Questionratings
from rest_framework import viewsets
from .serializers import UserSerializer, PostSerializer, RepliesSerializer
from django.db.models import Avg,Sum


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
                userdetail=User.objects.get(email=email)
                request.session['user_id'] = userdetail.id
                return HttpResponseRedirect('/post/')

def HomeView(request):
    if request.method == 'GET':
        return render(request, 'myapp/post.html')


def MainpageView(request):
    if request.method == 'GET':
        return render(request, 'myapp/index.html', {'login_form': LoginForm(), 'register_form': RegisterForm()})


class PostList(ListView):
    # model = Post
    # template_name = 'myapp/post_list.html'

    def get(self, request):
        post_list = Post.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(post_list, 5)
        try:
            post = paginator.page(page)
        except PageNotAnInteger:
            post = paginator.page(1)
        except EmptyPage:
            post =paginator.page(paginator.num_pages)

        return render(request, 'myapp/post_list.html', {'post_list': post, 'rating_form': PostRateForm})


class PostDetail(View):

    def get(self, request, pk):
        post_detail = Post.objects.get(pk=pk)
        reply = Replies.objects.all()
        try:
            ratings = Postratings.objects.filter(post_id=pk).aggregate(Avg('rate'))
            return render(request, 'myapp/post_detail.html',
                           {'post_detail': post_detail, 'replyform': ReplyPostForm, 'reply': reply,
                            'rating': ratings, 'rating_form': PostRateForm})
        except:

            return render(request, 'myapp/post_detail.html',
                          {'post_detail': post_detail, 'replyform': ReplyPostForm, 'reply': reply, 'rating_form': PostRateForm})




    # def post(self, request, pk):
    #     reply_form = ReplyPostForm(request.POST)
    #
    #     if reply_form.is_valid():
    #         text = reply_form.cleaned_data['text']
    #         reply = Replies(text=text, post_id=pk)
    #         reply.save()
    #         return HttpResponse("Replied!")
    #     else:
    #         return HttpResponse("Couldn't Replied!")

    def post(self, request, pk):
        form = PostRateForm(request.POST)

        if form.is_valid():
            rate = form.cleaned_data['rate']
            if Postratings.objects.filter(post_id=pk).filter(user_id=request.session['user_id']).exists():
                Postratings.objects.filter(post_id=pk).filter(user_id=request.session['user_id']).update(rate=rate)
                return HttpResponse("Rated!!")
                # return HttpResponseRedirect('/post/?message=rated&post&%s' % (pk))
            else:
                rating = Postratings(rate=rate, user_id=request.session['user_id'], post_id=pk)
                rating.save()
                return HttpResponseRedirect('/post/?message=rated&post&%s' % (pk))
        else:
            return HttpResponse("Must rate from 1 to 5 only!!")


class PostCreate(CreateView):
    model = Post
    fields = ['title', 'text', 'created_date', 'publish_date']
    template_name = 'myapp/post_new.html'
    success_url = reverse_lazy('myapp:post_list')


class PostUpdate(UpdateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'myapp/post_edit.html'
    success_url = reverse_lazy('myapp:post_list')

    #     total = form.cleaned_data['total']
    #     # post.save()
    #     if Postratings.objects.filter(post_id = pk).exists():
    #         rating = Postratings.objects.get(post_id = pk)
    #         rating.total = rating.total + total
    #         rating.rater_count = rating.rater_count + 1
    #         rating.average = rating.total/rating.rater_count
    #         rating.save()
    #     else:
    #         rating = Postratings(total=total, rater_count=1, average=total, post_id=pk)
    #         rating.save()
    #     return HttpResponseRedirect('/post/?message=rated&post&%s' % (pk))
    # else:
    #     return HttpResponse("Please rate from 1 to 10 only!!!")
    #







class PostDelete(DeleteView):
    model = Post
    template_name = 'myapp/post_delete.html'
    success_url = reverse_lazy('myapp:post_list')


class ReplyList(ListView):
    template_name = 'myapp/reply_list.html'
    model = Replies
    def get(self, request, pk):
        replies = Replies.objects.filter(post_id=pk)
    #      post_reply = Post.objects.get(post_id=pk)
        return render(request, 'myapp/reply_list.html', {'replies': replies})


class ReplyDetail(DetailView):
    model = Replies
    template_name = 'myapp/reply_detail.html'
    def get(self, request, pk):
        replies = Replies.objects.get(post_id=pk)
        return render(request, 'myapp/reply_detail.html', {'replies':replies})


class ReplyCreate(CreateView):
    model = Replies
    fields = ['post', 'text', 'created_date']
    template_name = 'myapp/reply_new.html'
    success_url = reverse_lazy('myapp:post_list')


class ReplyUpdate(UpdateView):
    model = Replies
    fields = ['post', 'text']
    template_name = 'myapp/reply_edit.html'
    success_url = reverse_lazy('myapp:post_list')


class ReplyDelete(DeleteView):
    model = Replies
    template_name = 'myapp/reply_delete.html'
    success_url = reverse_lazy('myapp:post_list')


class QuestionListView(ListView):
    def get(self, request):
        question_list = Questions.objects.all()
        return render(request, 'myapp/question_list.html', {'question_list': question_list})


class QuestionDetailView(DetailView):
    def get(self, request, pk):
        question_detail = Questions.objects.get(pk=pk)
        rating = Questionratings.objects.filter(question_id=pk).aggregate(Avg('rate'))
        # return HttpResponse(rating)
        return render(request, 'myapp/question_detail.html',
                      {'question_detail': question_detail, 'rating_form': QuestionRateForm, 'rating': rating})

    def post(self, request, pk):
        form = QuestionRateForm(request.POST)
        if form.is_valid():
            rate = form.cleaned_data['rate']
            if Questionratings.objects.filter(question_id=pk).filter(user_id=request.session['user_id']).exists():
                Questionratings.objects.filter(question_id=pk).filter(user_id=request.session['user_id']).update(rate=rate)
                return HttpResponse("Rated!!")
            else:
                rating = Questionratings(rate=rate, user_id=request.session['user_id'], question_id=pk)
                rating.save()
                return HttpResponse("Rated!!")
        else:
            return HttpResponse("Must rate from 1 to 5 only!!")


class QuestionCreate(CreateView):
    model = Questions
    fields = ['question', 'publish_date']
    template_name = 'myapp/question_new.html'
    success_url = reverse_lazy('myapp:question-list')



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class RepliesViewSet(viewsets.ModelViewSet):
    queryset = Replies.objects.all()
    serializer_class = RepliesSerializer



