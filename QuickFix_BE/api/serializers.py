from rest_framework import serializers
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from .models import *
import json
import pandas as pd
from django.db.models import Q, F, Sum

class PatientSignupSerializer(serializers.ModelSerializer):
    repassword = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True)
    dob = serializers.DateField(write_only=True, required=False, allow_null=True)
    gender = serializers.CharField(write_only=True, required=False, allow_null=True)
    number = serializers.CharField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'repassword', 
            'fullname', 'dob', 'gender', 'number'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"err": "Email already in use."})
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"err": "Username already in use."})
          
        if data['password'] != data['repassword']:
            raise serializers.ValidationError({"err": "Passwords do not match."})
        
        if data['password'] != data['repassword']:
            raise serializers.ValidationError({"err": "Passwords do not match."})
            
        return data
        
    def create(self, validated_data):
        repassword = validated_data.pop('repassword')
        fullname = validated_data.pop('fullname')
        dob = validated_data.get('dob', None)
        gender = validated_data.get('gender', None)
        number = validated_data.get('number', None)
        
        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=fullname, 
                role=User.Role.CUSTOMER,
                is_active=False  
            )
            user.save()
            CustomerProfile.objects.create(
                user=user,
                date_of_birth=dob,
                gender=gender,
                phone_number=number
            )
            Cart.objects.create(
                customer = user,
                created_at = timezone.now()
            ) 
        return user
    
# user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id", "username", "first_name", "email", "role"]
            
# customerprofile
class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = '__all__'  
# supplier
class SupplierSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= Supplier
        fields = "__all__"

# batches
class BatchSimpleSerializer(serializers.ModelSerializer):
    supplier_name = serializers.SerializerMethodField()
    class Meta:
        model= ProductBatch
        fields = [
            "id",
            "product_id",
            "batch_number",
            "supplier_id",
            "supplier_name",
            "expiry_date",
            "stock_qty",
            "created_at",
        ]
    
    
    def get_supplier_name(self, obj):
        supp = Supplier.objects.get(pk = obj.supplier.id)
        return supp.name
    
# product
class ProductAutocompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields=['name', 'generic_name']
    
class ProductShopListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    stock = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
           'id',
           'category',
           'category_name',
           'name',
           'generic_name',
           'description',
           'price',
           'requires_prescription',
           'image_url',
           'stock',
        ]
        
    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
    
    def get_category_name(self, obj):
        cat = Category.objects.get(id = obj.category.id)
        return cat.name
    
    def get_stock(self, obj):
        batch = ProductBatch.objects.filter(product = obj)
        total = batch.aggregate(Sum('stock_qty'))
        return total
    
class ProductDetailSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)
    stock = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model= Product
        fields = "__all__"
        
    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        return fields + ["image_url", 'category_name', 'stock']
    
    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
    
    def get_category_name(self, obj):
        cat = Category.objects.get(id = obj.category.id)
        return cat.name
    
    def get_stock(self, obj):
        batch = ProductBatch.objects.filter(product = obj)
        total = batch.aggregate(Sum('stock_qty'))
        return total
    
class ProductDetailBatchSimpleSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)
    category_name = serializers.SerializerMethodField(read_only=True)
    batches = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model= Product
        fields= [
            'id',
            'category',
            'category_name',
            'name',
            'sku',
            'generic_name',
            'description',
            'dosage_form',
            'strength',
            'price',
            'minimum_stock',
            'requires_prescription',
            'image_url',
            'image',
            'is_active',
            'created_at',
            'batches',
        ]
    
    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
    
    def get_category_name(self, obj):
        cat = Category.objects.get(id = obj.category.id)
        return cat.name
    
    def get_batches(self, obj):
        batch = ProductBatch.objects.filter(product = obj)
        return BatchSimpleSerializer(batch, many=True, read_only = True).data
        
# category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        
# Cart Item
class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    class Meta:
        model= CartItem
        fields = "__all__"
        
    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        return fields + ["product"]
    
    def get_product(self, obj):
        prod = Product.objects.get(pk = obj.product.id)
        return ProductDetailSerializer(prod, read_only=True).data
    
# order item
class OrderItemSimpleSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    batch = serializers.SerializerMethodField()
    class Meta:
        model= OrderItem
        fields = [
            "id",
            "product",
            "batch",
            "quantity",
            "price_at_purchase",
        ]
    def get_batch(self, obj):
        return BatchSimpleSerializer(obj.batch, read_only=True).data
    def get_product(self, obj):
        return ProductDetailSerializer(obj.product, read_only=True).data
    
class OrderItemComplicatedSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    # batch = serializers.SerializerMethodField()
    class Meta:
        model= OrderItem
        fields = [
            "id",
            "product",
            "batch",
            "quantity",
            "price_at_purchase",
        ]
    # def get_batch(self, obj):
    #     return BatchSimpleSerializer(obj.batch, read_only=True).data
    def get_product(self, obj):
        return ProductDetailBatchSimpleSerializer(obj.product, read_only=True).data
    
# order
class OrderListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    profile = serializers.SerializerMethodField()
    class Meta:
        model= Order
        fields = [
            "id",
            "customer_id",
            "prescription",
            "channel",
            "status",
            "total_amount",
            "created_at",
            "updated_at",
            "user",
            "profile",
        ]
    
    def get_user(self, obj):
        return UserSerializer(obj.customer).data
    def get_profile(self, obj):
        return CustomerProfileSerializer(obj.customer.profile).data
        
    
class OrderDetailedSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    class Meta:
        model= Order
        fields = [
            "id",
            "customer",
            "prescription",
            "channel",
            "status",
            "total_amount",
            "created_at",
            "updated_at",
            "items",
        ]
    
    def get_items(self, obj):
        items = OrderItem.objects.filter(order = obj)
        return OrderItemSimpleSerializer(items, many=True, read_only = True).data
    

    

    