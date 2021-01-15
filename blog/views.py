import re
import markdown
from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', locals())


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    md = markdown.Markdown(extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        TocExtension(slugify=slugify),
    ])
    post.body = md.convert(post.body)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    post.toc = m.group(1) if m is not None else ''
    return render(request, 'blog/detail.html', locals())


def archive(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
        created_time__month=month)
    return render(request, 'blog/index.html', locals())


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', locals())


def tag(request, pk):
    t = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=t)
    return render(request, 'blog/index.html', locals())
