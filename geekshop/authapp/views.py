from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from .forms import ShopUserEditForm, ShopUserProfileEditForm
from .forms import ShopUserLoginForm
from .forms import ShopUserRegisterForm
from .models import ShopUser

class UserLoginView(LoginView):
    model = ShopUser
    template_name = 'authapp/login.html'
    form_class = ShopUserLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Вход в систему'

        return context

class UserLogoutView(LogoutView):
    next_page = 'index'


def register(request):
    title = 'Регистрация нового пользователя'
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('сообщение подтверждения отправлено')
                messages.success(request, 'Ссылка для активации аккаунта \
                отправлена на вашу электронную почту')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                print('ошибка отправки сообщения')
                messages.error(request, 'Ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('auth:login'))
        else:
            register_form = ShopUserRegisterForm(request.POST, request.FILES)
            context = {
                'title': title,
                'form': register_form,
            }
            return render(request, 'authapp/register.html', context)
    else:
        register_form = ShopUserRegisterForm()
        context = {
            'title': title,
            'form': register_form}
        return render(request, 'authapp/register.html', context)


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
            auth.login(request, user,
                       backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('index'))

@login_required
@transaction.atomic
def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(
            request.POST,
            request.FILES,
            instance=request.user
        )
        profile_form = ShopUserProfileEditForm(
            request.POST,
            instance=request.user.shopuserprofile
        )
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(
            instance=request.user.shopuserprofile
        )

    context = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form
    }

    return render(request, 'authapp/edit.html', context)
