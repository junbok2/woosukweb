from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings # 게시판 추가
from django.utils import timezone

class MyAccountManager(BaseUserManager):
    # 일반 user 생성, username 이 userID를 의미함
    def create_user(self, email, username, name, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must have an userID.")
        if not name:
            raise ValueError("Users must have an name.")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 관리자 User 생성
    def create_superuser(self, email, username, name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            name=name,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser, PermissionsMixin):
    # 기본 필드
    email = models.EmailField(verbose_name='이메일', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=40, null=False, blank=False)
    create_at = models.DateTimeField(verbose_name='가입일', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='최근 로그인', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # 사용자 정보 관련 추가 필드
    university = models.CharField(max_length=120, null=True)
    major = models.CharField(max_length=120, null=True)
    address = models.CharField(max_length=120, null=True)

    birthdate = models.DateField(null=True)  # 생년월일
    wk_user_type = models.CharField(max_length=30, null=True)  # 신분구분(WK_USER_TYPE)
    modify_ip = models.GenericIPAddressField(null=True)  # 수정IP
    password = models.CharField(max_length=180, null=True)  # 패스워드
    start_date = models.DateTimeField(null=True)  # 사용시작일시
    end_date = models.DateTimeField(null=True)  # 사용종료일시
    department_code = models.CharField(max_length=30, null=True)  # 부서코드
    department_name = models.CharField(max_length=30, null=True)  # 부서명

    # 주소 및 연락처 관련 추가 필드
    postal_code = models.CharField(max_length=10, null=True)  # 우편번호
    address_detail = models.CharField(max_length=120, null=True)  # 주소
    input_id = models.CharField(max_length=30, null=True)  # 입력ID
    phone_number = models.CharField(max_length=20, null=True)  # 휴대전화번호
    telephone_number = models.CharField(max_length=20, null=True)  # 전화번호

    # 권한 및 기타 정보 관련 추가 필드
    permission = models.CharField(max_length=30, null=True)  # 권한

    remarks = models.TextField(null=True)  # 비고
    modify_id = models.CharField(max_length=30, null=True)  # 수정ID
    member_image = models.ImageField(upload_to='profile_images/', null=True)  # 회원 이미지
    input_ip = models.GenericIPAddressField(null=True)  # 입력IP
    input_date = models.DateTimeField(default=timezone.now)
    modify_date = models.DateTimeField(auto_now=True)  # 수정일시
    withdraw = models.BooleanField(default=False)  # 탈퇴여부
    withdraw_id = models.CharField(max_length=30, null=True)  # 탈퇴ID
    withdraw_ip = models.GenericIPAddressField(null=True)  # 탈퇴IP
    withdraw_date = models.DateTimeField(null=True)  # 탈퇴일시

    # 대학 및 학적 정보 관련 추가 필드
    wk_colg = models.CharField(max_length=30, null=True)  # 소속대학(WK_COLG)
    student_number = models.CharField(max_length=30, null=True)  # 학번(재학생)
    wk_sex = models.CharField(max_length=10, null=True)  # 성별(WK_SEX)

    objects = MyAccountManager()  # 헬퍼 클래스 사용

    USERNAME_FIELD = 'email'  # 로그인 ID로 사용할 필드
    REQUIRED_FIELDS = ['username', 'name']  # 필수 작성 필드

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_lable):
        return True

# 게시판
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Notice(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
