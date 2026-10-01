from django.contrib.messages.api import success
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
app_name = 'blog'

urlpatterns = [
    path('', views.index, name="index"),
    path('posts/', views.post_list, name="post_list"),
    path('posts/<str:category>/',views.post_list, name="post_list_category"),
    path('posts/detail/<int:id>', views.post_detail, name="post_detail"),
    path('posts/<post_id>/comment', views.post_comment, name="post_comment"),
    path('ticket/', views.ticket, name="ticket"),
    path('postform/', views.post_form, name="Post_form"),
    path('search', views.post_search, name="post_search"),
    path('profile/', views.profile, name="profile"),
    path('popular-posts/', views.popular_posts, name="popular_posts"),
    path('profile/create_post/', views.create_post, name="create_post"),
    path('profile/create_post/<post_id>', views.edit_post, name='edit_post'),
    path('profile/delete_post/<post_id>', views.delete_post, name="delete_post"),
    path('profile/delete_image/<image_id>', views.delete_image, name="delete_image"),
    path('login/', views.log_in, name="login"),
    # path('login/', auth_views.LoginView.as_view(template_name='blog/registration/login.html'), name="login"),
    path('logout/', views.log_out, name="logout"),
    path('password-change/', views.password_change, name="password_change"),
# path('password-change/', auth_views.PasswordChangeView.as_view(template_name='blog/registration/password_change.html', success_url=reverse_lazy('blog:password_change_done')), name="password_change"),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='blog/registration/password_change_done.html'), name="password_change_done"),
    path('password-reset/', views.reset_password, name="password_reset"),
    # path('password-reset/', auth_views.PasswordResetView.as_view(template_name='blog/registration/password_reset_form.html',success_url=reverse_lazy('blog:password_reset_done'),email_template_name='blog/registration/password_reset_email.html',), name="password_reset"),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='blog/registration/password_reset_done.html'), name="password_reset_done"),
    path('password-reset/<int:user_id>/<str:token>/',views.password_reset_confirm, name="password_reset_confirm"),
    # path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='blog/registration/password_reset_confirm.html',success_url=reverse_lazy('blog:password_reset_complete')), name="password_reset_confirm"),
    # path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='blog/registration/password_reset_complete.html'), name="password_reset_complete"),
    path('register/', views.register, name="register"),
    path('account/edit', views.edit_account, name="edit_account"),
    path('user-information/<int:user_id>',views.user_information, name="user_information"),
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact")
]
