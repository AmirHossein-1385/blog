import jdatetime
from django.db import models
from django.db.models import CharField, OneToOneRel, OneToOneField
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.urls import reverse
from django_resized import ResizedImageField
import os
import uuid
from django.template.defaultfilters import slugify


# managers
class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
        REJECTED = 'RJ', 'Rejected'

    CATEGORY_CHOICES = (
        ('تکنولوژی','تکنولوژی'),
        ('زبان برنامه نویسی','زبان برنامه نویسی'),
        ('هوش مصنوعی','هوش مصنوعی'),
        ('یلاکچین','یلاکچین'),
        ('سایر','سایر'),
    )


    # relations
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts", verbose_name="نویسنده")
    # data fields
    title = models.CharField(max_length=250, verbose_name="عنوان")
    description = models.TextField(verbose_name="توضیخات")
    slug = models.SlugField(max_length=250, verbose_name="اسلاگ")
    # date
    publish = jmodels.jDateTimeField(default=timezone.now, verbose_name="تاریخ انتشار")
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)
    # choice fields
    status = models.CharField(max_length=2,choices=Status.choices, default=Status.DRAFT, verbose_name="وضعیت")
    reading_time = models.PositiveIntegerField(verbose_name="زمان مطالعه")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="سایر")
    # objects = models.Manager()
    objects = jmodels.jManager()
    Published = PublishManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]
        verbose_name = "پست"
        verbose_name_plural = "پست ها"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Ticket(models.Model):
    message = models.TextField(verbose_name="پیام")
    name = models.CharField(max_length=250, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    phone = models.CharField(max_length=11, verbose_name="شماره تماس")
    subject = models.CharField(verbose_name="موضوع")

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="پست")
    name = models.CharField(max_length=250, verbose_name="Name")
    body = models.TextField(verbose_name="Comment text")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    active = models.BooleanField(default=False, verbose_name="وضعیت")

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return f"{self.name}:{self.post}"


def get_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('post_image', jdatetime.datetime.now().strftime('%Y/%m'), filename)


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images", verbose_name="تصویر")
    image_file = ResizedImageField(upload_to=get_upload_path, size=(200, 200), quality=100, crop=['middle', 'center'])
    title = models.CharField(max_length=250, verbose_name="عنوان", null=True, blank=True)
    description = models.TextField(verbose_name="توضیحات", null=True, blank=True)
    created = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]
        verbose_name = "تصویر"
        verbose_name_plural = "تصاویر"

    def __str__(self):
        if self.title:
            return self.title

        elif self.image_file.name:
            return self.image_file.name

        else:
            return "No image/No title"


def get_upload_photo_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('account_images', jdatetime.datetime.now().strftime('%Y/%m'), filename)

class Account(models.Model):
    user = OneToOneField(User, related_name="account", on_delete=models.CASCADE)
    date_of_birth = jmodels.jDateField(verbose_name="تاریخ تولد",null=True, blank=True)
    bio = models.TextField(verbose_name="بایو",null=True, blank=True)
    photo =ResizedImageField(upload_to=get_upload_photo_path,size=(200, 200), quality=100, crop=['middle', 'center'],null=True, blank=True)
    job = models.CharField(max_length=250, verbose_name="شغل",null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "اکانت"
        verbose_name_plural = "اکانت ها"


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token =models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
