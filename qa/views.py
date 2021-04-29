from django.shortcuts import render, HttpResponseRedirect, Http404
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import ListView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm
from .models import Organization, CustomUser, TPKey, TPKeysProduct


class OrganizationView(ListView):
    model = Organization


def signup(request, *args, **kwargs):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            key = request.POST['tp_key']
            tp_key = TPKey.objects.get(key=key)
            organization_title = tp_key.organization_title
            new_user = CustomUser.objects.create_user(username=request.POST['username'], email=request.POST['email'],
                                                      password=request.POST['password'],
                                                      is_superuser=0, first_name=request.POST['first_name'],
                                                      last_name=request.POST['last_name'], is_staff=0, is_active=1,
                                                      organization_title=organization_title)
            new_user.save()

            return HttpResponseRedirect(reverse(get_main_page))
            # //TODO make automatic authorization after registration
    else:
        form = UserRegisterForm(request.POST)
        return render(request, 'register_page.html', {'form': form, })


@require_GET
def get_main_page(request, *args, **kwargs):
    return render(request, 'main_page.html')


@login_required
def get_account_page(request, *args, **kwargs):
    if request.method == "GET":
        pass
        user = CustomUser.objects.get(username=request.user)
        organization = user.organization_title.title
        client = user.last_name + ' ' + user.first_name
        return render(request, 'account_page.html', {'organization': organization, 'client': client})




