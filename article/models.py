from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from slugify import slugify
# from django.utils.text import slugify


# Create your models here.
class ArticleColumn(models.Model):
    """
    文章栏目数据模型：一个用户对应多个文章栏目
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_column', verbose_name="用户")
    column = models.CharField(max_length=200, verbose_name="文章分类")
    created = models.DateField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.column


class ArticlePost(models.Model):
    """
    文章内容管理数据模型：
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=500)
    column = models.ForeignKey(ArticleColumn, on_delete=models.CASCADE, related_name="article_column")
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """
        对id、slug建立索引，通过这两个索引获取文章对象
        """
        ordering = ("-updated",)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        重写save方法
        :param args:
        :param kwargs:
        :return:
        """
        self.slug = slugify(self.title)
        super(ArticlePost, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        通过重写save方法，获取文章url
        reverse()、避免硬编码的写法、url是从path到name，reverse是从name到path.
        :return:
        """
        return reverse("article:article_detail", args=[self.id, self.slug])

    def get_url_path(self):
        return reverse("article:article_content", args=[self.id, self.slug])


# class Comment(models.Model):
#     article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE, related_name="comments")
#     commentator = models.CharField(max_length=90)
#     body = models.TextField()
#     created = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ('-created',)
#
#     def __str__(self):
#         return "Comment by {0} on {1}".format(self.commentator.username, self.article)
#
#
# class ArticleTag(models.Model):
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tag")
#     tag = models.CharField(max_length=500)
#
#     def __str__(self):
#         return self.tag
