from django.shortcuts import render, HttpResponseRedirect, Http404, redirect
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import ListView
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from rest_framework.parsers import JSONParser

from .forms import UserRegisterForm, RequestCreationForm, MessageSendForm
from .models import Organization, CustomUser, TPKey, TPKeysProduct, Product, Request, Correspondence
from .serializers import RequestSerializer, CorrespondenceSerializer


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

        message_form = MessageSendForm()

        # List of client's requests
        requests = Request.objects.filter(client=user).order_by('-registration_date')


        # Pagination
        paginator = Paginator(requests, 10, allow_empty_first_page=True)
        page_number = request.GET.get('page')
        if not page_number:
            page_number = 1
        page_obj = paginator.get_page(page_number)

        ids = list()
        for i in page_obj.object_list:
            ids.append(i.id)
        answers = Correspondence.objects.filter(req__in=ids).order_by('date').order_by('id').select_related('from_user')

        return render(request, 'account_page.html', {'organization': organization, 'client': client,
                                                     'req_form': req_form, 'message_form': message_form,
                                                     'page_obj': page_obj, 'last_page': paginator.num_pages,
                                                     'answers': answers})


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
            ans = Correspondence.objects.create(req=req, from_user=client, answer=request.POST['problem'])
            return HttpResponseRedirect(reverse(get_account_page))


@require_POST
def send_message(request, *args, **kwargs):
    if request.method == "POST":
        req_id = request.GET.get('request_id')
        req_query = Request.objects.get(pk=req_id)

        mes_form = MessageSendForm(request.POST)
        if mes_form.is_valid():
            client = CustomUser.objects.get(username=request.user)
            ans = Correspondence.objects.create(req=req_query, from_user=client, answer=request.POST['answer'])
            return HttpResponseRedirect(reverse('account'))

