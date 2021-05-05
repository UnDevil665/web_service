from django.shortcuts import render, HttpResponseRedirect, Http404
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import ListView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from rest_framework.parsers import JSONParser

from .forms import UserRegisterForm, RequestCreationForm
from .models import Organization, CustomUser, TPKey, TPKeysProduct, Product, Request
from .serializers import RequestSerializer


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
        # Client's information
        user = CustomUser.objects.get(username=request.user)
        organization = user.organization_title.title
        client = user.last_name + ' ' + user.first_name

        # List of available products to client's company
        keys = TPKey.objects.filter(organization_title=organization).values('id')
        products = TPKeysProduct.objects.filter(key_id_id__in=keys).values('product_id')
        products = Product.objects.filter(pk__in=products)

        req_form = RequestCreationForm()
        # adding list of available products to view
        req_form.fields["product"].queryset = products

        # List of client's requests
        requests = Request.objects.filter(client=user).order_by('-registration_date')
        serializer = RequestSerializer(requests, many=True)
        print(serializer.data[0])
        print(serializer.data)

        return render(request, 'account_page.html', {'organization': organization, 'client': client,
                                                     'req_form': req_form, 'data': serializer.data})


@require_POST
def send_request(request, *args, **kwargs):
    if request.method == "POST":
        req_form = RequestCreationForm(request.POST)
        if req_form.is_valid():
            client = CustomUser.objects.get(username=request.user)
            organization = Organization.objects.get(title=client.organization_title.title)
            product = Product.objects.get(product=request.POST['product'])
            req = Request.objects.create(client=client, client_organization=organization,
                                         problem=request.POST['problem'], product=product)
            return HttpResponseRedirect(reverse(get_account_page))



