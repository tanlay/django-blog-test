from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from django.views.decorators.http import require_POST
from .forms import CommentForm
from django.contrib import messages


@require_POST
def comment(request, post_pk):
    #先获取被评论的文章
    post = get_object_or_404(Post, pk=post_pk)
    # django将用户提交的数据封装在requset.POST中，是一个字典对象
    form = CommentForm(request.POST)
    # 当调用form.is_valid()时，django自动检查表单是否符合要求
    if form.is_valid():
        # 利用表单生成Comment模型实例，不提交到数据库
        comment = form.save(commit=False)
        # 关联评论和被评论的文章
        comment.post = post
        # 保存到数据库，调用模型实例save()方法
        comment.save()
        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')
        # 重定向到post详情页，
        # 当 redirect 函数接收一个模型的实例时
        # 它会调用这个模型实例的 get_absolute_url 方法，
        return redirect(post)

    # 检查数据不合法，渲染一个预览页面，展示表单错误
    # 被评论的文章post也传给了模板，因为需要根据post来生成表单
    context = {
        'post': post,
        'form': form,
    }
    messages.add_message(request, messages.ERROR, '评论发表失败！', extra_tags='danger')
    return render(request, 'comments/preview.html', locals())
