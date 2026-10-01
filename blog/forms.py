from django import forms
from django.contrib.auth.models import User

from .models import Comment, Post, Account


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ("پیشنهاد", "پیشنهاد"),
        ("انتقاد", "انتقاد"),
        ("گزارش مشکل", "گزارش")
    )
    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'placeholder': 'نام', 'class': 'name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'ایمیل'}))
    phone = forms.CharField(max_length=11, required=True, widget=forms.TextInput(attrs={'placeholder': 'شماره تلفن'}))
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("شماره تلفن عددی نیست")
            else:
                return phone


class CommentForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name) < 3:
                raise forms.ValidationError("نام کوتاه هست")
            else:
                return name

    class Meta:
        model = Comment
        fields = ['name', 'body']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'نام', 'class': 'comment_name'}),
            'body': forms.TextInput(attrs={'placeholder': 'متن', 'class': 'comment_body'})
        }


class PostForm(forms.ModelForm):
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise forms.ValidationError("تایتل باید بیشتر از 3 حرف باشه")
        else:
            return title

    def clean_reading_time(self):
        reading_time = self.cleaned_data.get('reading_time')
        if reading_time <= 0:
            raise forms.ValidationError("لطفا یک تایم معتبر برای تایم مطالعه وارد کنید")
        else:
            return reading_time

    class Meta:
        model = Post
        fields = ['author', 'title', 'description', 'reading_time']


class SearchForm(forms.Form):
    query = forms.CharField()


class CreatePostForm(forms.ModelForm):
    image1 = forms.ImageField(label="تصویر اول")
    image2 = forms.ImageField(label="تصویر دوم")

    class Meta:
        model = Post
        fields = ['title', 'description', 'reading_time','category']


# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=250, required=True)
#     password = forms.CharField(max_length=250, required=True, widget=forms.PasswordInput)


class UserRegisterForm(forms.ModelForm):
    password =forms.CharField(max_length=20, widget=forms.PasswordInput, label="password")
    password2 =forms.CharField(max_length=20, widget=forms.PasswordInput, label="repeat password")
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name', 'email']

    def clean_password2(self):
        cd =self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("پسورد ها با هم مطابقت ندارند")
        return cd['password2']

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class EditAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['date_of_birth', 'bio', 'photo', 'job']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class ChangePassword(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget = forms.PasswordInput())
    repeat_password = forms.CharField(widget = forms.PasswordInput())
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')
        if password != repeat_password:
            raise forms.ValidationError("پسورد ها یکی نیستند")

        return cleaned_data

class PasswordResetEmailForm(forms.Form):
    email = forms.EmailField()

class PasswordResetConfirm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    repeat_password = forms.CharField(widget=forms.PasswordInput())

    def clean_password2(self):
        cleaned_data = super().clean()
        password = self.cleaned_data.get('password1')
        repeat_password = self.cleaned_data.get('password2')
        if password != repeat_password:
            raise forms.ValidationError("پسورد ها یکی نیستند")
        return repeat_password