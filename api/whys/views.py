from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import AttributeName, AttributeValue, Attribute, Product, ProductAttributes, Image, ProductImage, Catalog
from .serializers import AttributeNameSerializer, AttributeValueSerializer, AttributeSerializer, ProductSerializer, ProductAttributesSerializer, ImageSerializer, ProductImageSerializer, CatalogSerializer


class ImportView(APIView):
    def post(self, request):
        data = request.data


class DetailModulesView(APIView):
    def get(self, request, module_name):
        return


class DetailModuleIdView(APIView):
    def get(self, request, module_name, id):
        return
