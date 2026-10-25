from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    LoginForm, 
    PsswordResetRequestForm, 
    SetNewPasswordForm, 
    UserRegistrationForm,
    PasswordChangeForm,
    UserEditForm,
    ProfileEditForm
)
from .models import Profile, Contact
# from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username = cd['username'],
                password = cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request,'succesfully login your account')
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect (next_url)
                    return redirect ('dashboard')
                
                else:
                    messages.error(request,'this user is not active')
            else:
                messages.error(request,'user not found')
    else:
        form = LoginForm()
    return render (request,'account/login.html',{
        'form':form
    })


def user_logout(request):
    logout(request)
    return render (request,'account/logout.html',{
        'section':'dashboard'
    })

@login_required
def dashboard(request):
    return render (request,'account/dashboard.html')

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request,'succesfully changed your password')
            return redirect ('dashboard')
    else:
        form = PasswordChangeForm(user=request.user)
    return render (request,'account/password_change.html',{
        'form':form
    })


def password_reset_request(request):
    if request.method == 'POST':
        form = PsswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = request.get_host()
            reset_link = f'http://{domain}/account/password_reset_confirm/{uid}/{token}'
            subject = 'password reset request'
            message = f'{user.username} clickh this link and reset your password\n {reset_link}'
            send_mail(
                subject,
                message,
                None,
                [email]
            )
            messages.success(request,'check you email and reset your password')
            return redirect('password_reset_request')

    else:
        form = PsswordResetRequestForm()
    return render (request,'account/password_reset_request.html',
                   {
                        'form':form
                   })

@login_required
def password_reset_confirm(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = SetNewPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()

                messages.success(request,'succesfully chenge your password')
                return redirect ('login')
        else:
            form = SetNewPasswordForm()
        return render (request,'account/password_reset_confirm.html',
                       {
                           'form':form
                       })
    else:
        messages.error(request, 'this link is no valid')
        return redirect ('password_reset_request')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data.get('confirm_password')
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            messages.success (request,f'succesfully register {new_user.username} your account')
            return redirect ('login')
    else:
        user_form = UserRegistrationForm()
    return render (request,'account/register.html',{
        'user_form':user_form
    })


def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(  instance=request.user,  data=request.POST  )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,  files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success (request,'profile update succesfully')
        else:
            messages.error(request,'error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(  request,  'account/edit.html',  {
        'user_form': user_form,
        'profile_form': profile_form})

User = get_user_model()
@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render (request,'account/user_list.html',{
        'section':'people', 
        'users':users
    })

@login_required
def user_detail(request, username):
    user = get_object_or_404(
        User,
        username=username,
        is_active=True
    )
    return render (request,'account/user_detail.html',{
        'section':'people',
        'user':user
    })

@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
            else:
                Contact.objects.filter(
                    user_from=request.user,
                    user_to=user
                ).delete()
            return JsonResponse ({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse ({'status':'error'})
    return JsonResponse ({'status':'error'})
                                