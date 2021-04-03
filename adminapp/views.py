from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from authapp.models import Users
from adminapp.forms import UserAdminRegistration, UserAdminUpdate
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator


@user_passes_test(lambda user: user.is_active)
def index(request):
    return render(request, 'adminapp/admin.html')

class UserCreateView(CreateView):
    model = Users
    template_name = 'adminapp/admin-users-create.html'
    form_class = UserAdminRegistration()
    success_url = reverse_lazy('adminapp:read')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

# @user_passes_test(lambda user: user.is_active)
# def users_create(request):
#     if request.method == 'POST':
#         form = UserAdminRegistration(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:read'))
#     else:
#         form = UserAdminRegistration()
#     content = {
#         'form': form
#     }
#     return render(request, 'adminapp/admin-users-create.html', content)


# @user_passes_test(lambda user: user.is_active)
# def users_read(request):
#     content = {
#         'users': Users.objects.all()
#     }
#     return render(request, 'adminapp/admin-users-read.html', content)

class UsersListView(ListView):
    model = Users
    template_name = 'adminapp/admin-users-read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda user: user.is_active)
# def users_update(request, id):
#     user = Users.objects.get(id=id)
#     if request.method == 'POST':
#         form = UserAdminUpdate(data=request.POST, files=request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('adminapp:read'))
#     else:
#         form = UserAdminUpdate(instance=user)
#
#     content = {
#         'form': form,
#         'current_user': user
#     }
#     return render(request, 'adminapp/admin-users-update-delete.html', content)

class UserUpdateView(UpdateView):
    model = Users
    template_name = 'adminapp/admin-users-update-delete.html'
    form_class = UserAdminUpdate
    success_url = reverse_lazy('adminapp:read')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# @user_passes_test(lambda user: user.is_active)
# def users_delete(request, id):
#     user = Users.objects.get(id=id)
#     user.is_active = False
#     user.save()
#     return HttpResponseRedirect(reverse('adminapp:read'))


class UserDeleteView(DeleteView):
    model = Users
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('adminapp:read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
