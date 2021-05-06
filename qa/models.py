from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth.models import AbstractUser


class Organization(models.Model):
    inn = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=100, unique=True)
    index = models.CharField(max_length=6, blank=True)
    address = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=18, null=False)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class Product(models.Model):
    product = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.product

    def __str__(self):
        return self.product


class TPKey(models.Model):
    key = models.CharField(max_length=6, unique=True)
    products = models.ManyToManyField(Product, through="TPKeysProduct", through_fields=('key_id', 'product_id'))
    organization_title = models.ForeignKey(Organization, to_field="title", on_delete=models.RESTRICT)

    def __unicode__(self):
        return self.key

    def __str__(self):
        return self.key


class TPKeysProduct(models.Model):
    key_id = models.ForeignKey(TPKey, on_delete=models.RESTRICT)
    product_id = models.ForeignKey(Product, on_delete=models.RESTRICT)

    def __unicode__(self):
        return self.id

    def __str__(self):
        return self.key_id


class CustomUser(AbstractUser):
    organization_title = models.ForeignKey(Organization, to_field='title',
                                           on_delete=models.RESTRICT, related_name='clients_organization', null=False)


class Status(models.Model):
    status = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.status


class Request(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    client_organization = models.ForeignKey(Organization, to_field='title', on_delete=models.RESTRICT,
                                            related_name='request_clients_organization')

    product = models.ForeignKey(Product, to_field='product', on_delete=models.RESTRICT,
                                related_name='requests_product')

    registration_date = models.DateTimeField(auto_now_add=True)

    problem = models.TextField()

    status = models.ForeignKey(Status, to_field='status', on_delete=models.RESTRICT, default='Открыта')

    def __unicode__(self):
        return self.id

    def __str__(self):
        return self.id


class Correspondence(models.Model):
    req = models.ForeignKey(Request, on_delete=models.RESTRICT)
    answer = models.TextField()
    from_user = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id
