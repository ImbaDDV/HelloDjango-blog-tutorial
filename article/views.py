# 引入markdown模块
import markdown
import re
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from .models import ArticlePost, Category, Tag
from django.core.paginator import Paginator
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User
# 引入HttpResponse
from django.http import HttpResponse


# 创建文章
def article_create(request):
    # 判断用户是否提交表单
    if request.POST:
        # 将用户提交数据传入表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断用户输入数据是否符合模型要求
        if article_post_form.is_valid():
            # 保存数据，暂不提交至数据库
            new_article = article_post_form.save(commit=False)
            # 制定id=1的用户为作者
            new_article.author = User.objects.get(id=1)
            # 保存数据至数据库
            new_article.save()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        else:
            # 引入HttpResponse
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {
            'article_post_form': article_post_form,
            'function': '写文章',
        }
        # 返回模板
        return render(request, 'article/createorupdate.html', context)


# 修改文章
def article_update(request, pk):
    # 获取文章信息
    article = ArticlePost.objects.get(id=pk)
    # 判断用户是否提交表单
    if request.POST:
        # 将用户提交数据传入表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断用户输入数据是否符合模型要求
        if article_post_form.is_valid():
            # 更新修改时间
            article.modified_time = timezone.now
            # 更新修改后标题和正文
            article.title = request.POST['title']
            article.body = request.POST['body']
            # 保存数据至数据库
            article.save()
            # 完成后返回到文章列表
            return redirect("article:article_detail", pk=pk)
        else:
            # 引入HttpResponse
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {
            'article_post_form': article_post_form,
            'article': article,
            'function': '修改文章',
        }
        # 返回模板
        return render(request, 'article/createorupdate.html', context)


# 文章列表
def article_list(request):
    article_list = ArticlePost.objects.all()

    # 对post_list进行分页处理,每页显示4篇文章
    paginator = Paginator(article_list, 2)

    # 获取表单中当前页
    page = request.GET.get('page')

    # 将导航对象相应的页码内容返回给 Post
    articles = paginator.get_page(page)

    context = {
        'article_list': article_list,
        'articles': articles,
    }

    return render(request, 'article/list.html', context)


def article_detail(request, pk):
    article = get_object_or_404(ArticlePost, pk=pk)

    # 阅读量+1
    article.increase_views()

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        # 记得在顶部引入 TocExtension 和 slugify
        TocExtension(slugify=slugify),
    ])
    article.body = md.convert(article.body)

    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    article.toc = m.group(1) if m is not None else ''

    context = {
        'article': article,
    }

    return render(request, 'article/detail.html', context)


# 获取相应年月的归档文章
def archive(request, year, month):
    article_list = ArticlePost.objects.filter(created_time__year=year,
                                              created_time__month=month
                                              )

    context = {
        'article_list': article_list,
    }

    return render(request, 'article/list.html', context)


def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)

    article_list = ArticlePost.objects.filter(category=cate)

    context = {
        'article_list': article_list,
    }

    return render(request, 'article/list.html', context)


def tag(request, pk):
    # 记得在开始部分导入 Tag 类
    t = get_object_or_404(Tag, pk=pk)
    article_list = ArticlePost.objects.filter(tags=t)

    context = {
        'article_list': article_list,
    }

    return render(request, 'article/list.html', context)
