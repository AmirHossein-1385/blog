from django import template
from blog.models import *
from ..models import Post, Comment
from django.db.models import Count,Max,Min
register = template.Library()
from markdown import markdown
from django.utils.safestring import mark_safe


@register.simple_tag()
def total_posts():
    return Post.Published.count()


@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()



@register.inclusion_tag('partials/latest_posts.html')
def latest_posts(count=4):
    posts = Post.Published.order_by('-publish')[:count]
    context = {
        'posts': posts
    }
    return context


@register.inclusion_tag('partials/First posts.html')
def first_posts(count=4):
    f_posts = Post.Published.order_by('publish')[:count]
    context = {
        'f_posts': f_posts
    }
    return context


@register.simple_tag()
def most_popular_posts(count=5):
    return Post.Published.annotate(comments_count=Count('comments')).order_by('-comments_count')[:count]


@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))


@register.simple_tag()
def max_reading_time():
    state = Post.Published.aggregate(max=Max('reading_time'))
    result = state.get('max')
    return result or 0


@register.simple_tag()
def min_reading_time():
    state = Post.Published.aggregate(min=Min('reading_time'))
    result = state.get('min')
    return result or 0


Bad_words = ['احمق', 'بد', 'زشت']


@register.filter()
def censorship(value):
    text = value
    for word in Bad_words:
        text = text.replace(word, '*' * len(word))
    return mark_safe(text)


@register.simple_tag()
def The_most_active_user():
    active = User.objects.annotate(count_post = Count('user_posts')).order_by('-count_post').first()
    return active


@register.simple_tag()
def random_post():
    post = Post.Published.order_by('?').first()

    return post