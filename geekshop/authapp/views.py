from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm
from authapp.forms import ShopUserRegisterForm
from authapp.forms import ShopUserEditForm
from django.contrib import auth
from django.urls import reverse

from authapp.models import ShopUser
from mainapp.views import get_basket


def login(request):
    title = 'Вход в систему'

    login_form = ShopUserLoginForm(data=request.POST or None)

    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST'and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index'))



    content = {
        'title': title,
        'login_form': login_form,
        'next': next,
    }
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    title = 'Регистрация нового пользователя'
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('сообщение подтверждения отправлено')
                return HttpResponseRedirect(reverse('auth:verify_link_send'))
            else:
                print('ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('auth:verify_link_failed'))
        else:
            register_form = ShopUserRegisterForm()
            context = {
                'title': title,
                'register_form': register_form}
            return render(request, 'authapp/register.html', context)
    else:
        register_form = ShopUserRegisterForm()
        context = {
            'title': title,
            'register_form': register_form}
        return render(request, 'authapp/register.html', context)


def edit(request):
    title = 'Редактирование данных пользователя'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES,
                                     instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)

    content = {
        'title': title,
        'edit_form': edit_form,
        'basket': get_basket(request.user),
    }

    return render(request, 'authapp/edit.html', content)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.username}'

    message = f'Ссылка для подтверждения учетной записи {user.username} \
    на портале {settings.DOMAIN_NAME}: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email],
                     fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and \
                not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('index'))

def link_send_fail(request):
    message = {
        'text': 'Cообщение на электронную почту не отправлено',
        'link': 'auth:register',
        'link_description': 'Перейти к регистрации пользователя'
    }
    context = {
        'title': 'ошибка',
        'message': message,
    }
    return render(request, 'authapp/verify_link_send.html', context)

def link_send_sucsess (request):
    message = {
        'text': 'Ссылка для активации учетной записи отправлена \
        на вашу электронную почту',
        'link': 'auth:login',
        'link_description': 'Войти'
    }
    context = {
        'title': 'завершение регистрации пользователя',
        'message': message,
    }
    return render(request, 'authapp/verify_link_send.html', context)

