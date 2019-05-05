from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Post
from .forms import EmailPostForm


############# Function view ##############################
# def post_list(request):
#
#     # posts = Post.published.all()
#     # return render(request, 'blog/post/list.html', {'posts': posts})
#     # 引入分页功能
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 3) # 每页三个post
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#
#     return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})
############################################################################


######## Classed view ################################################
class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})


def post_share(request, post_id):
    # retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # 通过窗口提交数据
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # 表单域经过了合法性验证
            cd = form.cleaned_data
            # send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}{} 推荐你阅读 "{}"'.format(cd['name'], cd['email'], post.title)
            message = '阅读 "{}" 在 {}\n\n{}的 评论: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject,message, 'hflag@163.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})
