from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import RegisterView, LoginView, MainpageView, HomeView
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', MainpageView, name='main'),
    path('home/', login_required(HomeView)),
    path('register/', RegisterView, name='register'),
    path('login/', LoginView, name='login'),

    path('post/', views.PostList.as_view(), name='post_list'),
    path('post/<int:pk>', views.PostDetail.as_view(), name='post-detail'),
    path('post-new/', views.PostCreate.as_view(), name='post_new'),
    path('post-edit/<int:pk>', views.PostUpdate.as_view(), name='post-edit'),
    path('post-delete/<int:pk>', views.PostDelete.as_view(), name='post-delete'),

    path('reply/<int:pk>', views.ReplyList.as_view(), name='reply_list'),
    path('reply/<int:pk>', views.ReplyDetail.as_view(), name='reply_detail'),
    path('reply-new/', views.ReplyCreate.as_view(), name='reply_new'),
    path('reply-edit/<int:pk>', views.ReplyUpdate.as_view(), name='reply_edit'),
    path('reply-delete/<int:pk>', views.ReplyDelete.as_view(), name='reply_delete'),

    path('question/', views.QuestionListView.as_view(), name='question-list'),
    path('question/<int:pk>', views.QuestionDetailView.as_view(), name='question-detail'),
    path('question-new/', views.QuestionCreate.as_view(), name='question-new'),

]