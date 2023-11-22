# Generated by Django 4.2.6 on 2023-11-22 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='이메일')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('name', models.CharField(max_length=40)),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='가입일')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='최근 로그인')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('university', models.CharField(max_length=120, null=True)),
                ('major', models.CharField(max_length=120, null=True)),
                ('address', models.CharField(max_length=120, null=True)),
                ('birthdate', models.DateField(null=True)),
                ('wk_user_type', models.CharField(max_length=30, null=True)),
                ('modify_ip', models.GenericIPAddressField(null=True)),
                ('password', models.CharField(max_length=30, null=True)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('department_code', models.CharField(max_length=30, null=True)),
                ('department_name', models.CharField(max_length=30, null=True)),
                ('postal_code', models.CharField(max_length=10, null=True)),
                ('address_detail', models.CharField(max_length=120, null=True)),
                ('input_id', models.CharField(max_length=30, null=True)),
                ('phone_number', models.CharField(max_length=20, null=True)),
                ('telephone_number', models.CharField(max_length=20, null=True)),
                ('permission', models.CharField(max_length=30, null=True)),
                ('remarks', models.TextField(null=True)),
                ('modify_id', models.CharField(max_length=30, null=True)),
                ('member_image', models.ImageField(null=True, upload_to='profile_images/')),
                ('input_ip', models.GenericIPAddressField(null=True)),
                ('input_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('modify_date', models.DateTimeField(auto_now=True)),
                ('withdraw', models.BooleanField(default=False)),
                ('withdraw_id', models.CharField(max_length=30, null=True)),
                ('withdraw_ip', models.GenericIPAddressField(null=True)),
                ('withdraw_date', models.DateTimeField(null=True)),
                ('wk_colg', models.CharField(max_length=30, null=True)),
                ('student_number', models.CharField(max_length=30, null=True)),
                ('wk_sex', models.CharField(max_length=10, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
