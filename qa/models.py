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
    organization = models.ForeignKey(Organization, on_delete=models.RESTRICT)

    def __unicode__(self):
        return self.key

    def __str__(self):
        return self.key


class TPKeysProduct(models.Model):
    key = models.ForeignKey(TPKey, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)

    def __unicode__(self):
        return self.id

    def __str__(self):
        return self.key


class CustomUser(AbstractUser):
    organization = models.ForeignKey(Organization,
                                     on_delete=models.RESTRICT, related_name='clients_organization_pk', null=False)

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.last_name + ' ' + self.first_name


class Status(models.Model):
    status = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.status


class Request(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    organization = models.ForeignKey(Organization, on_delete=models.RESTRICT,
                                     related_name='request_clients_organization')

    product = models.ForeignKey(Product, on_delete=models.RESTRICT, related_name='requests_product')

    registration_date = models.DateTimeField(auto_now_add=True)

    problem = models.TextField()

    status = models.ForeignKey(Status, on_delete=models.RESTRICT)

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)


class Correspondence(models.Model):
    req = models.ForeignKey(Request, on_delete=models.RESTRICT)
    answer = models.TextField()
    from_user = models.ForeignKey(CustomUser, on_delete=models.RESTRICT)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
