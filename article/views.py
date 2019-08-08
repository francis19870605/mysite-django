from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import ArticleColumn, ArticlePost
from .forms import ArticleColumnForm, ArticlePostForm


# Create your views here.
@login_required(login_url="/account/login")
@csrf_exempt
def article_column(request):
    """
    后台管理-栏目管理-增加文章栏目
    :param request:
    :return:
    """
    if request.method == "GET":
        columns = ArticleColumn.objects.filter(user=request.user)
        column_form = ArticleColumnForm()
        return render(request, "article/column/article_column.html", {"columns": columns, "column_form": column_form})

    if request.method == "POST":
        column_name = request.POST.get('column', None)
        # column_name = request.POST['column']
        columns = ArticleColumn.objects.filter(user=request.user.id, column=column_name)

        if columns:
            return HttpResponse("2")
        else:
            ArticleColumn.objects.create(user=request.user, column=column_name)
            return HttpResponse("1")


# require_POST装饰器只允许次函数接受POST请求
@login_required(login_url="/account/login")
@require_POST
@csrf_exempt
def rename_article_column(request):
    """
    后台管理-栏目管理-编辑文章栏目
    :param request:
    :return:
    """
    column_name = request.POST['column_name']
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.column = column_name
        line.save()
        return HttpResponse("1")
    except:
        return HttpResponse("0")


@login_required(login_url="/account/login")
@require_POST
@csrf_exempt
def del_article_column(request):
    """
    后台管理-栏目管理-删除文章栏目
    :param request:
    :return:
    """
    column_id = request.POST['column_id']
    try:
        line = ArticleColumn.objects.get(id=column_id)
        line.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("0")


@login_required(login_url="/account/login")
@csrf_exempt
def article_post(request):
    """
    后台管理-发布文章
    :param request:
    :return:
    """
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                new_article.column = request.user.article_column.get(id=request.POST['column_id'])
                new_article.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        article_post_form = ArticlePostForm()
        article_columns = request.user.article_column.all()
        return render(request, "article/column/article_post.html", {"article_post_form": article_post_form,
                                                                    "article_columns": article_columns})


@login_required(login_url="/account/login")
def article_list(request):
    """
    后台管理-文章列表
    :param request:
    :return:
    """
    articles_list = ArticlePost.objects.filter(author=request.user)
    # 根据查询到的对象articles_list创建分页的实例对象，每页2个
    paginator = Paginator(articles_list, 18)
    # 获得当前浏览器GET请求的参数page值(页码数值)
    page = request.GET.get('page')
    try:
        # page() Paginator对象的一个方法 获取指定页面内容 参数必须是大于或等于1的整数
        current_page = paginator.page(page)
        # object_list Page对象的属性 获取该页所有的对象列表
        articles = current_page.object_list
    # 捕获异常(请求的页码数值不是整数)
    except PageNotAnInteger:
        current_page = paginator.page(1)
        articles = current_page.object_list
    # 捕获异常(请求的页码数值为空或者在rul参数中没有page)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
        articles = current_page.object_list
    return render(request, "article/column/article_list.html", {"articles": articles, "page": current_page})


@login_required(login_url="/account/login")
def article_detail(request, id, slug):
    """
    后台管理-文章列表-文章详细页面
    :param request:
    :param id:
    :param slug:
    :return:
    """
    print(request.GET.get)
    article = get_object_or_404(ArticlePost, id=id, slug=slug)
    return render(request, "article/column/article_detail.html", {"article": article})


@login_required(login_url="/account/login")
@require_POST
@csrf_exempt
def del_article(request):
    """
    后台管理-文章列表-删除文章
    :param request:
    :return:
    """
    article_id = request.POST['article_id']
    try:
        article = ArticlePost.objects.get(id=article_id)
        article.delete()
        return HttpResponse("1")
    except:
        return HttpResponse("2")


@login_required(login_url="/account/login")
@csrf_exempt
def redit_article(request, article_id):
    """
    后台管理-文章列表-新编辑文章
    :param request:
    :return:
    """
    if request.method == "GET":
        article_columns = request.user.article_column.all()
        article = ArticlePost.objects.get(id=article_id)
        this_article_form = ArticlePostForm(initial={"title": article.title})
        this_article_column = article.column
        return render(request, "article/column/redit_article.html", {"article": article,
                                                                     "article_columns": article_columns,
                                                                     "this_article_column": this_article_column,
                                                                     "this_article_form": this_article_form})
    else:
        redit_article = ArticlePost.objects.get(id=article_id)
        try:
            redit_article.column = request.user.article_column.get(id=request.POST['column_id'])
            redit_article.title = request.POST['title']
            redit_article.body = request.POST['body']
            redit_article.save()
            return HttpResponse("1")
        except:
            return HttpResponse("2")
