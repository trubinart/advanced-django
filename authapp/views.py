from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import UsersLoginForm, UsersRegistration, UsersProfileForm
from django.contrib import auth
from django.urls import reverse
from basketapp.models import Basket
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from authapp.models import Users

def login(request):
    if request.method == 'POST':
        form = UsersLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main'))
    else:
        form = UsersLoginForm()

    content = {
        'title': 'GeekShop - Авторизация',
        'form': form
    }
    return render(request, 'authapp/login.html', content)


def register(request):
    if request.method == 'POST':
        form = UsersRegistration(data=request.POST)
        if form.is_valid():
            user = form.save()
            if send_verify_mail(user):
                print('Cообщение подтверждения отправлено')

                content_key = {
                    'activation_key': user.activation_key,
                }
                return render(request, 'authapp/login.html', content_key)

            else:
                print('Ошибка отправки сообщения')
                return HttpResponseRedirect(reverse('auth:register'))
    else:
        form = UsersRegistration()

    content = {
        'title': 'GeekShop - Регистрация',
        'form': form
    }
    return render(request, 'authapp/register.html', content)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UsersProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        form = UsersProfileForm(instance=request.user)

    content = {
        'form': form,
        'baskets': Basket.objects.filter(user=request.user),
    }
    return render(request, 'authapp/profile.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username} на портале \
    {settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

def verify(request, email, activation_key):
    try:
        user = Users.objects.get(email=email)
        if user.activation_key == activation_key and user.is_activation_key_expired:
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            print(f'Ошибка активации юзера: {user}')
            return render(request, 'authapp/verification.html')

    except Exception as error:
        print(f'error activation user : {error.args}')
        return HttpResponseRedirect(reverse('main'))

    except:
        pass