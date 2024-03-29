from django import forms

from myapp.models import Postratings, Replies, Questionratings, Post


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control form-control-md'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control form-control-md'}))
# class SignupForm(forms.Form):
#     name = forms.CharField(label='Your Name', max_length=100)


class RegisterForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control form-control-md'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control form-control-md'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class':'form-control form-control-md'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control form-control-md'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'form-control form-control-md'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control form-control-md'}))
    # birth_date = forms.DateField(null=True, blank=True)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'photo', 'created_date', 'publish_date']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['photo'].required = False

class PostRateForm(forms.ModelForm):
    class Meta:
        model = Postratings
        fields = ['rate']


class QuestionRateForm(forms.ModelForm):
    class Meta:
        model = Questionratings
        fields = ['rate']

class ReplyPostForm(forms.ModelForm):
    class Meta:
        model = Replies
        fields = ['text', 'created_date']