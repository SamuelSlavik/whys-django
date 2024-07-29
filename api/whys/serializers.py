from rest_framework import serializers
from .models import AttributeName, AttributeValue, Attribute, Product, ProductAttributes, Image, ProductImage, Catalog


# In the attribute case, I decided to return directly the values instead of the actual objects of the attribute name and value
# In the product and catalog, you can see other approaches
class AttributeSerializer(serializers.ModelSerializer):
    nazev_atributu = serializers.SerializerMethodField()
    hodnota_atributu = serializers.SerializerMethodField()

    class Meta:
        model = Attribute
        fields = '__all__'

    def get_nazev_atributu(self, obj):
        return obj.nazev_atributu.nazev

    def get_hodnota_atributu(self, obj):
        return obj.hodnota_atributu.hodnota


class AttributeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeName
        fields = '__all__'


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = '__all__'


class ProductAttributesSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer()

    class Meta:
        model = ProductAttributes
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    obrazek = ImageSerializer()

    class Meta:
        model = ProductImage
        fields = '__all__'


# Showcasing 2 approaches how to reach information about attributes and images linked to product
# Returning array of items both for attributes and images
class ProductSerializer(serializers.ModelSerializer):
    attributes = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_attributes(self, obj):
        product_attributes = ProductAttributes.objects.filter(product=obj)
        return AttributeSerializer([product_attribute.attribute for product_attribute in product_attributes], many=True).data

    def get_images(self, obj):
        product_images = ProductImage.objects.filter(product=obj)
        image_ids = [pi.obrazek.id for pi in product_images]
        images = Image.objects.filter(id__in=image_ids)
        return ImageSerializer(images, many=True).data


# Catalogs also return full objects of linked products and attributes, not only their ids or other values
class CatalogSerializer(serializers.ModelSerializer):
    obrazek = ImageSerializer()
    products = ProductSerializer(many=True)
    attributes = AttributeSerializer(many=True)

    class Meta:
        model = Catalog
        fields = '__all__'
