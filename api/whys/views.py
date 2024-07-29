from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from .models import AttributeName, AttributeValue, Attribute, Product, ProductAttributes, Image, ProductImage, Catalog
from .serializers import *


# General view for parsing input data
# Accepts JSON with different models and their data.
# All data is parsed, it doesnt crash, just pass, when some data are not valid
# For better testing (and your validation of my implementation), returns arrays of successfully parsed or skipped models names
# For purposes of this project, handles both create and update methods
class ImportView(APIView):
    def post(self, request):
        data = request.data
        # Arrays of successfully parsed data and errors for testing and validation purposes
        processed_data = {
            'success': [],
            'error': []
        }

        # Helper function for checking if the object already exists and should be updated or created
        def get_instance_or_none(model, id):
            try:
                return model.objects.get(id=id)
            except model.DoesNotExist:
                return None

        # Loop through items in payload
        for item in data:
            model_name = list(item.keys())[0]
            model_data = item[model_name]

            # PROCCESING OF A SINGLE MODEL:
            # - try to find the exsiting instace
            # - if it exists, update the found object
            # - If it doesnt exists, create new one
            try:
                # ATTRIBUTE NAME ###################################################################################
                if model_name == 'AttributeName':
                    instance = get_instance_or_none(AttributeName, model_data.get('id'))
                    if instance:
                        for field, value in model_data.items():
                            setattr(instance, field, value)
                        instance.save()
                    else:
                        AttributeName.objects.create(**model_data)

                # ATTRIBUTE VALUE ###################################################################################
                elif model_name == 'AttributeValue':
                    instance = get_instance_or_none(AttributeValue, model_data.get('id'))
                    if instance:
                        for field, value in model_data.items():
                            setattr(instance, field, value)
                        instance.save()
                    else:
                        AttributeValue.objects.create(**model_data)

                # ATTRIBUTE ###################################################################################
                elif model_name == 'Attribute':
                    instance = get_instance_or_none(Attribute, model_data.get('id'))
                    if instance:
                        if 'nazev_atributu_id' in model_data:
                            model_data['nazev_atributu'] = get_instance_or_none(AttributeName, model_data.pop('nazev_atributu_id'))
                        if 'hodnota_atributu_id' in model_data:
                            model_data['hodnota_atributu'] = get_instance_or_none(AttributeValue, model_data.pop('hodnota_atributu_id'))
                        for field, value in model_data.items():
                            setattr(instance, field, value)
                        instance.save()
                    else:
                        model_data['nazev_atributu'] = get_instance_or_none(AttributeName, model_data.pop('nazev_atributu_id'))
                        model_data['hodnota_atributu'] = get_instance_or_none(AttributeValue, model_data.pop('hodnota_atributu_id'))
                        Attribute.objects.create(**model_data)

                # PRODUCT ###################################################################################
                elif model_name == 'Product':
                    instance = get_instance_or_none(Product, model_data.get('id'))
                    if instance:
                        for field, value in model_data.items():
                            setattr(instance, field, value)
                        instance.save()
                    else:
                        Product.objects.create(**model_data)

                # PRODUCT ATTRIBUTE ###################################################################################
                elif model_name == 'ProductAttributes':
                    instance = get_instance_or_none(ProductAttributes, model_data.get('id'))
                    if instance:
                        if 'attribute' in model_data:
                            model_data['attribute'] = get_instance_or_none(Attribute, model_data.pop('attribute'))
                        if 'product' in model_data:
                            model_data['product'] = get_instance_or_none(Product, model_data.pop('product'))
                        for field, value in model_data.items():
                            setattr(instance, field, value)
                        instance.save()
                    else:
                        model_data['attribute'] = get_instance_or_none(Attribute, model_data.pop('attribute'))
                        model_data['product'] = get_instance_or_none(Product, model_data.pop('product'))
                        ProductAttributes.objects.create(**model_data)

                # IMAGE ###################################################################################
                elif model_name == 'Image':
                    instance = get_instance_or_none(Image, model_data.get('id'))
                    if instance:
                        for field, value in model_data.items():
                            setattr(instance, field, value)
                        instance.save()
                    else:
                        Image.objects.create(**model_data)

                # PRODUCT IMAGE ###################################################################################
                elif model_name == 'ProductImage':
                    instance = get_instance_or_none(ProductImage, model_data.get('id'))
                    if instance:
                        if 'product' in model_data:
                            model_data['product'] = get_instance_or_none(Product, model_data.pop('product'))
                        if 'obrazek_id' in model_data:
                            model_data['obrazek'] = get_instance_or_none(Image, model_data.pop('obrazek_id'))
                        for field, value in model_data.items():
                            setattr(instance, field, value)
                        instance.save()
                    else:
                        model_data['product'] = get_instance_or_none(Product, model_data.pop('product'))
                        model_data['obrazek'] = get_instance_or_none(Image, model_data.pop('obrazek_id'))
                        ProductImage.objects.create(**model_data)

                # CATALOG ###################################################################################
                elif model_name == 'Catalog':
                    instance = get_instance_or_none(Catalog, model_data.get('id'))

                    if instance:
                        if 'nazev' in model_data:
                            instance.nazev = model_data.pop('nazev')
                        if 'obrazek' in model_data:
                            instance.obrazek = get_instance_or_none(Image, model_data.pop('obrazek'))
                        if 'products_ids' in model_data:
                            instance.products.set(model_data.pop('products_ids'))
                        if 'attributes' in model_data:
                            instance.attributes.set(model_data.pop('attributes'))
                        instance.save()
                    else:
                        if 'nazev' not in model_data:
                            raise ValueError("The 'nazev' field is required when creating a new Catalog.")
                        if 'obrazek' in model_data:
                            model_data['obrazek'] = get_instance_or_none(Image, model_data.pop('obrazek'))
                        if 'products_ids' in model_data:
                            products = model_data.pop('products_ids')
                        else:
                            products = []
                        if 'attributes_ids' in model_data:
                            attributes = model_data.pop('attributes_ids')
                        else:
                            attributes = []
                        instance = Catalog.objects.create(**model_data)
                        instance.products.set(products)
                        instance.attributes.set(attributes)

                processed_data['success'].append(model_name)
            except KeyError as e:
                processed_data['error'].append(f"{model_name}: {str(e)}")
            except Exception as e:
                processed_data['error'].append(f"{model_name}: {str(e)}")

        return Response(processed_data, status=status.HTTP_200_OK)


# Returns array of models with the given name
# If invalid model name, returns 400 error
class DetailModelsView(APIView):
    def get(self, request, model_name):
        # For better user experience
        model_map = {
            'attributename': AttributeName,
            'attributevalue': AttributeValue,
            'attribute': Attribute,
            'product': Product,
            'productattributes': ProductAttributes,
            'image': Image,
            'productimage': ProductImage,
            'catalog': Catalog
        }

        try:
            model = model_map[model_name.lower()]
            queryset = model.objects.all()
            serializer_class = globals()[f"{model.__name__}Serializer"]
            serializer = serializer_class(queryset, many=True)
            return Response(serializer.data)
        except KeyError:
            return Response({'error': 'Invalid model name'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Return detailed info for the model with given name and id
# If invalid model name, returns 400 error
# If not found item with given ID, returns 404 error
class DetailModelIdView(APIView):
    def get(self, request, model_name, id):
        # For better user experience
        model_map = {
            'attributename': AttributeName,
            'attributevalue': AttributeValue,
            'attribute': Attribute,
            'product': Product,
            'productattributes': ProductAttributes,
            'image': Image,
            'productimage': ProductImage,
            'catalog': Catalog
        }

        try:
            model = model_map[model_name.lower()]
            instance = model.objects.get(id=id)
            serializer_class = globals()[f"{model.__name__}Serializer"]
            serializer = serializer_class(instance)
            return Response(serializer.data)
        except KeyError:
            return Response({'error': 'Invalid model name'}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'error': f'{model_name} with id {id} not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Delete all models view for testing purposes
class DeleteAllView(APIView):
    def delete(self, request):
        models = [
            AttributeName,
            AttributeValue,
            Attribute,
            Product,
            ProductAttributes,
            Image,
            ProductImage,
            Catalog
        ]

        try:
            with transaction.atomic():
                for model in models:
                    model.objects.all().delete()

            return Response({
                'message': 'Successfully deleted all data'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
