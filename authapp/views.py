from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import UsersLoginForm, UsersRegistration, UsersProfileForm
from django.contrib import auth
from django.urls import reverse
from basketapp.models import Basket
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from authapp.models import Users
from django.contrib.auth.views import LoginView

# def login(request):
#     if request.method == 'POST':
#         form = UsersLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('main'))
#     else:
#         form = UsersLoginForm()
#
#     content = {
#         'title': 'GeekShop - Авторизация',
#         'form': form
#     }
#     return render(request, 'authapp/login.html', content)

class UserLoginView(LoginView):
    template_name = 'authapp/login.html'
    authentication_form = UsersLoginForm

    def get_success_url(self):
        return reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data()
        context['title'] = 'GeekShop - Авторизация'
        return context

# def register(request):
#     if request.method == 'POST':
#         form = UsersRegistration(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('auth:login'))
#     else:
#         form = UsersRegistration()
#
#     content = {
#         'title': 'GeekShop - Регистрация',
#         'form': form
#     }
#     return render(request, 'authapp/register.html', content)

class UserRegisterView(CreateView):
    model = Users
    template_name = 'authapp/register.html'
    form_class = UsersRegistration
    success_url = reverse_lazy('auth:login')


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
