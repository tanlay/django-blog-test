import markdown
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import strip_tags



class Category(models.Model):
    name = models.CharField('分类名', max_length=100)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('标签名', max_length=100)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField('标题', max_length=170)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    updated_time = models.DateTimeField('修改时间')
    brief = models.CharField('摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    class Meta:
        """配置后台字段"""
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    # 定义方法使updated_time自动更新
    def save(self, *args, **kwargs):
        self.updated_time = timezone.now()
        # 实例化一个markdown类，用于渲染body文本
        # 摘要也不需要生成文章目录，去掉了TOC
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # strip_tags去掉了html标签
        self.brief = strip_tags(md.convert(self.body)[:54])
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
