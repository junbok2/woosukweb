from django.shortcuts import render, redirect, get_object_or_404
from .api import (recruitment_api, pagebutton, recruitment_detail_api, job_api, job_detail_api,
                  youthpolicy_detail_api, youthpolicy_search_api)
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, Page
from django.http import JsonResponse
from .forms import UserRegistrationForm, UserLoginForm, PostForm
from .models import User, Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, "woosukplus/index.html")

def noticeboard(request):
    return render(request, "woosukplus/noticeboard.html")

def recruitment(request):
    value = recruitment_api()
    page = request.GET.get('page')
    paginator = Paginator(value, 20)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        page_obj = paginator.page(page)
    custom_range = pagebutton(page,paginator.num_pages)
    return render(request, "woosukplus/recruitment.html", {'page_obj':page_obj, 'paginator':paginator, 'custom_range':custom_range})

def recruitment_detail(request, boardid):
    board = recruitment_detail_api(boardid)
    return render(request, "woosukplus/recruitment_detail.html", {'board':board})
def job(request):
    return render(request, "woosukplus/job.html")
def job_search(request):
    search_value = request.POST.get('search_value')
    pageIndex = request.POST.get('pageIndex')
    searchJobCd = request.POST.get('searchJobCd')
    value = job_api(pageIndex,search_value,searchJobCd)

    context = {'value': value, 'pageIndex':pageIndex}
    return JsonResponse(context)

def job_detail(request, pageIndex, boardid):
    board = job_detail_api(pageIndex, boardid)
    return render(request, "woosukplus/job_detail.html", {'board': board})

def youthpolicy(request):
    return render(request, "woosukplus/youthpolicy.html")
def youthpolicy_search(request):
    pageIndex = request.POST.get('pageIndex')
    search_value = request.POST.get('search_value')
    value = youthpolicy_search_api(pageIndex, search_value)

    context = {'value': value, 'pageIndex': pageIndex}
    return JsonResponse(context)
def youthpolicy_detail(request, boardid, pageIndex ):
    board = youthpolicy_detail_api(pageIndex, boardid)
    return render(request, "woosukplus/youthpolicy_detail.html", {'board': board})
def education(request):
    return render(request, "woosukplus/education.html")

def join(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()

    return render(request, 'woosukplus/join.html',  {'form': form, 'errors': form.errors})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)  # 수정: 'request' 객체만 전달
                return redirect('index')  # 'index' 페이지로 리디렉션
    else:
        form = UserLoginForm()
    return render(request, 'woosukplus/login.html', {'form': form})


def logout_view(request):
    logout(request)  # 사용자 로그아웃
    return redirect('index')

# 게시판
def post_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)  # 페이지당 10개의 게시물 표시
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'woosukplus/post_list.html', {'posts': posts})

@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'woosukplus/create_post.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # 현재 게시물보다 이전 글과 다음 글을 가져옵니다.
    previous_post = Post.objects.filter(id__lt=post_id).order_by('-id').first()
    next_post = Post.objects.filter(id__gt=post_id).order_by('id').first()

    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
    }

    return render(request, 'woosukplus/post_detail.html', context)

def board_page(request):
    posts_per_page = 10  # 한 페이지에 표시할 게시글 수
    posts = Post.objects.all()  # 모든 게시글을 가져옵니다.

    paginator = Paginator(posts, posts_per_page)  # Paginator 객체 생성
    page_number = request.GET.get('page')  # URL에서 현재 페이지 번호를 가져옵니다.

    try:
        posts = paginator.page(page_number)  # 현재 페이지의 게시글들을 가져옵니다.
    except Exception as e:
        # 페이지 번호가 유효하지 않은 경우 또는 페이지 범위를 벗어난 경우 기본적으로 첫 번째 페이지를 보여줍니다.
        posts = paginator.page(1)

    return render(request, 'post_list.html', {'posts': posts, 'paginator': paginator})