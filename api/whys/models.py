from django.db import models


class AttributeName(models.Model):
    nazev = models.CharField(max_length=255, null=True, blank=True)
    kod = models.CharField(max_length=255, null=True, blank=True)
    zobrazit = models.BooleanField(default=False)


class AttributeValue(models.Model):
    hodnota = models.CharField(max_length=255)


class Attribute(models.Model):
    nazev_atributu = models.ForeignKey(AttributeName, on_delete=models.CASCADE)
    hodnota_atributu = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)


class Product(models.Model):
    nazev = models.CharField(max_length=255)
    description = models.TextField()
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    mena = models.CharField(max_length=10, null=True, blank=True)
    published_on = models.DateTimeField(null=True, blank=True)
    is_published = models.BooleanField(default=False)


class ProductAttributes(models.Model):
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Image(models.Model):
    obrazek = models.URLField()
    nazev = models.CharField(max_length=255, null=True, blank=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    obrazek = models.ForeignKey(Image, on_delete=models.CASCADE)
    nazev = models.CharField(max_length=255, blank=True, null=True)


class Catalog(models.Model):
    nazev = models.CharField(max_length=255)
    obrazek = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(Product)
    attributes = models.ManyToManyField(Attribute)