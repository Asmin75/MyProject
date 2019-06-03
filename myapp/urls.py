from django.urls import path
from django.contrib.auth.decorators import login_required


from .views import  RegisterView, LoginView, MainpageView, HomeView
from . import views

app_name = 'myapp'

urlpatterns = [
    # path('login/', LoginView, name='login'),
    path('', MainpageView),
    path('home/', login_required(HomeView)),
    # path('index/', IndexView, name='index'),
    path('register/', RegisterView, name='register'),
    path('login/', LoginView, name='login'),

    path('post/', views.PostList.as_view(), name='postlist'),
    # path('post/<int:pk>', views.PostDetail.as_view(), name='post_detail'),
    path('post-new/', views.PostCreate.as_view(), name='post_new'),
    # path('post-edit/<int:pk>', views.PostUpdate.as_view(), name='post_edit'),
    # path('post-delete/<int:pk>', views.PostDelete.as_view(), name='post_delete'),
    #
    # path('reply/', views.ReplyList.as_view(), name='reply_list'),
    # path('reply/<int:pk>', views.ReplyDetail.as_view(), name='reply_detail'),
    # path('reply-new/', views.ReplyCreate.as_view(), name='reply_new'),
    # path('reply-edit/<int:pk>', views.ReplyUpdate.as_view(), name='reply_edit'),
    # path('reply-delete/<int:pk>', views.ReplyDelete.as_view(), name='reply_delete'),
]