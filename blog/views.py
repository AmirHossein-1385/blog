import datetime
import paginator
from django.contrib.auth.forms import PasswordResetForm
from django.core import paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from psycopg.types import none
from .models import *
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
import secrets


# Create your views here.


def index(request):
    return render(request, "blog/index.html")


def post_list(request,category=None):
    if category is not None:
        posts =Post.Published.filter(category=category)
    else:
        posts = Post.Published.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    context = {
        "posts": posts,
        "category": category,
    }
    return render(request, "blog/list.html", context)


# class PostListView(ListView):
#     queryset = Post.Published.all()
#     context_object_name = "posts"
#     paginate_by = 3
#     template_name = "blog/list.html"


def post_detail(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {
        "post": post,
        "form": form,
        "comments": comments,
    }
    return render(request, "blog/detail.html", context)


# class PostDetailView(DetailView):
#     model = Post
#     template_name = "blog/detail.html"


def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket_obj = Ticket.objects.create()
            cd = form.cleaned_data
            ticket_obj.message = cd['message']
            ticket_obj.name = cd['name']
            ticket_obj.email = cd['email']
            ticket_obj.phone = cd['phone']
            ticket_obj.subject = cd['subject']
            ticket_obj.save()
            return redirect("blog:index")
    else:
        form = TicketForm()
    return render(request, "forms/Ticket.html", {'form': form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    return render(request, "forms/Comment.html", context)


@login_required
def post_form(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:index')

    else:
        form = PostForm()

    context = {
        'form': form
    }
    return render(request, 'forms/Post.html', context)


# def post_search(request):
#     query = None
#     results = []
#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             results = Post.Published.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1).order_by('-similarity')
#
#         context = {
#             'query': query,
#             'results': results,
#         }
#         return render(request, 'blog/search.html', context)


def post_search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = \
                Post.Published.annotate(similarity=TrigramSimilarity('title', query),
                                        image_title=TrigramSimilarity('images__title', query)) \
                    .filter(Q(similarity__gt=0.1) | Q(image_title__gt=0.1)).order_by('-similarity', 'image_title')

        context = {
            'query': query,
            'results': results,
        }
        return render(request, 'blog/search.html', context)


@login_required
def profile(request):
    user = request.user
    posts = Post.objects.filter(author=user).all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)
    context = {
        'posts': posts,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('blog:profile')
    else:
        form = CreatePostForm()

    return render(request, 'forms/create_post.html', {"form": form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:profile')
    context = {
        'post': post
    }
    return render(request, 'forms/delete-post.html', context)


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect('blog:profile')
    else:
        form = CreatePostForm(instance=post)
    context = {
        'post': post,
        'form': form
    }
    return render(request, 'forms/create_post.html', context)


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    if image.post.author != request.user:
        messages.error(request, "شما اجازه حذف این تصویر رو ندارید")
    else:
        image.delete()
        messages.success(request,"عکس با موفقیت حذف شد")
    return redirect('blog:profile')


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('blog:profile')
#                 else:
#                     return HttpResponse("Your account is disabled")
#             else:
#                 return HttpResponse("You are not logged in")
#     else:
#         form = LoginForm()
#
#     context = {
#         'form': form
#     }
#     return render(request, 'forms/login.html', context)

def log_in(request):
    if request.method=='POST':
        form =LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect('blog:index')
    else:
        form =LoginForm()
    context = {
        'form': form
    }
    return render(request, 'blog/registration/login.html', context)

def log_out(request):
    logout(request)
    return redirect("blog:index")


def password_change(request):
    if request.method == 'POST':
        form = ChangePassword(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            if request.user.check_password(old_password):
                password = form.cleaned_data['password']
                request.user.set_password(password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                return redirect('blog:password_change_done')
            else:
                form.add_error('old_password', 'پسورد قدیمی شما معتبر نیست')
    else:
        form = ChangePassword()
    context = {
        'form': form
    }
    return render(request, 'blog/registration/password_change.html', context)


def reset_password(request):
    if request.method =='POST':
        form = PasswordResetEmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user =User.objects.get(email=email)
                token = secrets.token_urlsafe(32)
                PasswordResetToken.objects.create(user=user, token=token)
                reset_link = f"http://127.0.0.1:8000/blog/password-reset/{user.id}/{token}"
                print(reset_link)
                messages.success(request,"اگر این ایمیل ثبت شده باشد لینک بازیابی ارسال خواهد شد")
                return redirect('blog:index')
            except User.DoesNotExist:
                messages.success(request, "اگر کاربر با این ایمیل وجود داشته باشد لینک برایش ارسال خواهد شد")
                return redirect('blog:index')
    else:
        form = PasswordResetEmailForm()
    return render(request, 'blog/registration/password_reset_form.html', {"form": form, "validlink": True})


def password_reset_confirm(request, user_id, token):
    try:
        reset_token = PasswordResetToken.objects.get(user_id=user_id, token=token, used=False)
    except PasswordResetToken.DoesNotExist:
        messages.success(request, "لینک نامعتیر هست")
        return redirect('blog:index')
    if request.method == 'POST':
        form = PasswordResetConfirm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['repeat_password']
            user = reset_token.user
            user.set_password(password)
            user.save()
            reset_token.used = True
            reset_token.save()
            return redirect('blog:login')
    else:
        form = PasswordResetConfirm()

    return render(request,'blog/registration/password_reset_confirm.html',{'form':form, 'validlink': True})




def register(request):
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user =form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.create(user=user)
            return render(request, 'blog/registration/register_done.html',{'user':user})
    else:
        form = UserRegisterForm()
    context = {
        'form':form
    }
    return render(request, 'blog/registration/register.html',context)


@login_required
def edit_account(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        account_form = EditAccountForm(request.POST, files=request.FILES, instance=request.user.account)
        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            return redirect('blog:profile')
    else:
        user_form = EditUserForm(instance=request.user)
        account_form = EditAccountForm(instance=request.user.account)

    context = {
       "user_form": user_form,
        "account_form": account_form
    }
    return render(request, 'blog/registration/edit_account.html',context)


def user_information(request, user_id):
    user=get_object_or_404(User,id=user_id)
    context = {
        'user': user,
    }
    return render(request, 'blog/user_information.html', context)


def popular_posts(request):
    from django.db.models import Count
    posts = Post.Published.annotate(comments_count=Count('comments')).order_by('-comments_count')[:3]
    context = {
        'posts': posts,
    }
    return render(request, 'partials/popular_posts.html', context)


def about(request):
    return render(request, 'partials/about.html')

def contact(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            Ticket.objects.create(
                name=cd['name'],
                email=cd['email'],
                phone=cd['phone'],
                subject=cd['subject'],
                message=cd['message']
            )

            return redirect("blog:index")
    else:
        form = TicketForm()

    return render(request, "partials/contact.html", {"form": form})