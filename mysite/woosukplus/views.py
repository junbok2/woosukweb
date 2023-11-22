from django.shortcuts import render, redirect, get_object_or_404
from .api import (recruitment_api, pagebutton, recruitment_detail_api, job_api, job_detail_api,
                  youthpolicy_detail_api, youthpolicy_search_api)
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, Page
from django.http import JsonResponse
from .forms import UserRegistrationForm, UserLoginForm, PostForm, NoticeForm, UserProfileUpdateForm
from .models import User, Post, Notice
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    value_re = recruitment_api(5)
    notices = Notice.objects.order_by('-created_at')[:5]
    value_yo = youthpolicy_search_api(1, '', 5)
    return render(request, "woosukplus/index.html", {'value_re': value_re, 'value_yo': value_yo['youthPolicy'], 'notices': notices})


def recruitment(request):
    value = recruitment_api(600)
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
    board = recruitment_detail_api(boardid, 600)
    return render(request, "woosukplus/recruitment_detail.html", {'board':board})
def job(request):
    return render(request, "woosukplus/job.html")
def job_search(request):
    search_value = request.POST.get('search_value')
    pageIndex = request.POST.get('pageIndex')
    searchJobCd = request.POST.get('searchJobCd')
    value = job_api(pageIndex,search_value,searchJobCd)

    if search_value == '':
        search_value = 'all'
    if searchJobCd == '':
        searchJobCd = 'all'

    context = {'value': value, 'pageIndex':pageIndex, 'search_value':search_value, 'searchJobCd':searchJobCd}
    return JsonResponse(context)

def job_detail(request, pageIndex, boardid, search_value, searchJobCd):


    board = job_detail_api(pageIndex, boardid, search_value, searchJobCd)
    return render(request, "woosukplus/job_detail.html", {'board': board})

def youthpolicy(request):
    return render(request, "woosukplus/youthpolicy.html")
def youthpolicy_search(request):
    pageIndex = request.POST.get('pageIndex')
    search_value = request.POST.get('search_value')
    value = youthpolicy_search_api(pageIndex, search_value, 9)

    if search_value == '':
        search_value = 'all'

    context = {'value': value, 'pageIndex': pageIndex, 'search_value': search_value}
    return JsonResponse(context)
def youthpolicy_detail(request, boardid, pageIndex, search_value ):
    board = youthpolicy_detail_api(pageIndex, boardid, 9, search_value)
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
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, '이메일 또는 비밀번호가 일치하지 않습니다.')
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

#삭제
# woosukplus/views.py

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('post_list')

    return render(request, 'woosukplus/post_delete.html', {'post': post})

def noticeboard(request):
    notices = Notice.objects.all()
    paginator = Paginator(notices, 10)  # 페이지당 10개의 게시물 표시
    page = request.GET.get('page')
    notices = paginator.get_page(page)
    return render(request, 'woosukplus/noticeboard.html', {'notices': notices})



@login_required(login_url='login')
def create_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            new_notice = form.save(commit=False)
            new_notice.author = request.user
            new_notice.save()
            return redirect('noticeboard')
    else:
        form = NoticeForm()
    return render(request, 'woosukplus/create_notice.html', {'form': form})


def notice_detail(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)

    # 현재 게시물보다 이전 글과 다음 글을 가져옵니다.
    previous_notice = Notice.objects.filter(id__lt=notice_id).order_by('-id').first()
    next_notice = Notice.objects.filter(id__gt=notice_id).order_by('id').first()

    context = {
        'notice': notice,
        'previous_notice': previous_notice,
        'next_notice': next_notice,
    }

    return render(request, 'woosukplus/notice_detail.html', context)


def notice_delete(request,pk):
    notice = get_object_or_404(Notice, pk=pk)

    if request.method == 'POST':
        notice.delete()
        return redirect('noticeboard')

    return render(request, 'woosukplus/notice_delete.html', {'notice': notice})
def consulting(request):
    return render(request, "woosukplus/consulting.html")

def user_profile(request):
    return render(request, "woosukplus/user_profile.html")


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  # 프로필 페이지로 리다이렉트
    else:
        form = UserProfileUpdateForm(instance=request.user)

    return render(request, 'woosukplus/edit_profile.html', {'form': form})