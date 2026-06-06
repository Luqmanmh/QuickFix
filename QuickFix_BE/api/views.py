from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import generics, viewsets, permissions
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.db import transaction
from django.db.models import Q, F, Sum
from django.core.paginator import Paginator
from dotenv import load_dotenv
import math
import os
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from rest_framework.permissions import AllowAny
import random

load_dotenv()


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = User.objects.filter(username=username).first()
        if user is None:
            user = User.objects.filter(email=username).first()

        if user is None:
            raise AuthenticationFailed("User not Found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password!")

        if not user.is_active:
            raise AuthenticationFailed("This account is currently inactive.")

        tokens = RefreshToken.for_user(user)
        access_token = str(tokens.access_token)
        refresh_token = str(tokens)

        response = Response(
            {"username": user.username, "userid": user.id, "role": user.role}
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite="Lax",
            max_age=4 * 60 * 60,
            path="/",
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=not settings.DEBUG,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,
            path="/",
        )

        return response


class TokenRefreshCookieView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("Cookies:", request.COOKIES)
        refresh_token = request.COOKIES.get("refresh_token")
        print("Refresh token:", refresh_token)

        if not refresh_token:
            raise AuthenticationFailed("Refresh token cookie is missing.")

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)
            response = Response({"detail": "Token refreshed successfully."})

            response.set_cookie(
                key="access_token",
                value=new_access_token,
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                max_age=2 * 60 * 60,
                path="/",
            )

            return response

        except Exception:
            raise AuthenticationFailed("Invalid or expired refresh token.")


class SignupView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = PatientSignupSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        verification_link = (
            f"{os.getenv("ACT_URL")}/verify-email?uid={uid}&token={token}"
        )

        subject = "Verify your QuickFix Account"
        message = f"Hi {user.username},\n\nPlease verify your email by clicking the link below:\n{verification_link}"

        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )

        email.content_subtype = "plain"
        email.send(fail_silently=False)

    def create(self, request, *skip, **kwargs):
        response = super().create(request, *skip, **kwargs)
        response.data = {
            "detail": "Registration successful. Please check your email to verify your account."
        }
        return response


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")

        if not uidb64 or not token:
            return Response(
                {"err": "Missing verification parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # 1. Decode user ID
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response(
                {"err": "Invalid activation link."}, status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Check token validity
        if default_token_generator.check_token(user, token):
            if not user.is_active:
                user.is_active = True
                user.save()

            # 3. Automatically log them in by issuing HttpOnly JWT cookies
            tokens = RefreshToken.for_user(user)

            response = Response(
                {
                    "detail": "Email verified successfully!",
                    "username": user.username,
                    "userid": user.id,
                    "role": user.role,
                },
                status=status.HTTP_200_OK,
            )

            response.set_cookie(
                key="access_token",
                value=str(tokens.access_token),
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                max_age=15 * 60,
                path="/",
            )

            response.set_cookie(
                key="refresh_token",
                value=str(tokens),
                httponly=True,
                secure=not settings.DEBUG,
                samesite="Lax",
                max_age=7 * 24 * 60 * 60,
                path="/",
            )

            return response

        return Response(
            {"err": "Activation link is invalid or has expired."},
            status=status.HTTP_400_BAD_REQUEST,
        )


# -------------------------------------

class CategoryListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        cat = Category.objects.all().order_by("name")

        serial = CategorySerializer(cat, many=True)
        return Response(serial.data)


class SupplierListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        supp = Supplier.objects.all().order_by("name")

        serial = SupplierSerializer(supp, many=True)
        return Response(serial.data)  


class ProductAutocompleteView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        query = request.GET.get("query", "")

        prod = Product.objects.filter(Q(name__icontains=query) | Q(generic_name__icontains=query))
        
        serial = ProductAutocompleteSerializer(prod, many=True)
        return Response(serial.data)


class ProductShopItemListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        user = request.user
        query = request.GET.get("query", "")
        category = request.GET.get("category", "")
        dosage = request.GET.get("dosage")
        strength = request.GET.get("strength")
        price_low = request.GET.get("price_low")
        price_high = request.GET.get("price_high")
        presc = request.GET.get("presc")
        page_len = int(request.GET.get("page_len", 10))
        page = int(request.GET.get("page", 1))

        prod = (
            Product.objects.annotate(
                total_batch_stock=Sum("batches__stock_qty", default=0)
            )
            .filter(total_batch_stock__gt=F("minimum_stock"), is_active=True)
            .order_by("id")
        )

        if query:
            prod = prod.filter(
                Q(name__icontains=query) | Q(generic_name__icontains=query)
            )

        if dosage:
            prod = prod.filter(dosage_form__icontains=dosage)

        if price_low:
            prod = prod.filter(price__gte=price_low)
            
        if price_high:
            prod = prod.filter(price__lte=price_high)

        if presc == 'true':
            prod = prod.filter(requires_prescription=True)

        if category:
            prod = prod.filter(category_id__in=category)

        prod_paged = Paginator(prod, page_len)
        prod_page = prod_paged.get_page(page)

        serial = ProductShopListSerializer(prod_page, many=True)
        return Response(
            {
                "data": serial.data,
                "pagin": {
                    "current_page": prod_page.number,
                    "page_len": page_len,
                    "total_items": prod_page.paginator.count,
                    "total_page": prod_page.paginator.num_pages,
                },
            }
        )


class ProductManageListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        user = request.user
        query = request.GET.get("query", "")
        category = request.GET.get("category", "")
        presc = request.GET.get("presc")
        page_len = int(request.GET.get("page_len", 10))
        page = int(request.GET.get("page", 1))

        prod = (
            Product.objects
            .all()
            .order_by("id")
        )

        if query:
            prod = prod.filter(
                Q(name__icontains=query) | Q(generic_name__icontains=query) |
                Q(sku__icontains=query)
            )

        if presc == 'true':
            prod = prod.filter(requires_prescription=True)

        if category:
            prod = prod.filter(category_id__in=category)

        prod_paged = Paginator(prod, page_len)
        prod_page = prod_paged.get_page(page)

        serial = ProductDetailBatchSimpleSerializer(prod_page, many=True)
        return Response(
            {
                "data": serial.data,
                "pagin": {
                    "current_page": prod_page.number,
                    "page_len": page_len,
                    "total_items": prod_page.paginator.count,
                    "total_page": prod_page.paginator.num_pages,
                },
            }
        )



class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id, format=None):
        item = Product.objects.get(pk = id)
        
        serial = ProductDetailSerializer(item)
        return Response(serial.data)
    
    
class CartItemsView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def post(self, request, format=None):
        user = request.user
        item_id = request.data.get('item_id')
        quant = request.data.get('quant', 1)
        
        if not item_id:
            return Response({"details" : "No item ID provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        cart = Cart.objects.get(customer = user)
        prod = Product.objects.get(pk = item_id)    
        
        if not prod:
            return Response({'details': ' No Product with that ID exists'}, status=status.HTTP_404_NOT_FOUND)
             
        with transaction.atomic():
    
            item, created = CartItem.objects.get_or_create(
                cart = cart,
                product = prod,
                defaults={'quantity' : 0}
            )
            
            item.quantity += quant
            item.save()
            
        return Response({'details' : 'product added to cart'}, status=status.HTTP_201_CREATED)
    
    def get(self, request, format=None):
        user = request.user
        page = int(request.GET.get("page", 1))
        
        cart = Cart.objects.get(customer = user)
        items = CartItem.objects.filter(cart = cart).order_by('product')
        items_paged = Paginator(items, 15)
        items_page = items_paged.get_page(page)
        
        serial = CartItemSerializer(items_page, many=True)
        return Response(
            {
                "data": serial.data,
                "pagin": {
                    "current_page":items_page.number,
                    "page_len": 15,
                    "total_items":items_page.paginator.count,
                    "total_page":items_page.paginator.num_pages,
                },
            }
        )
        
    def put(self, request, format=None):
        user = request.user
        item_id = request.GET.get('item_id')
        quant = request.GET.get('quant')
        
        item = CartItem.objects.get(pk = item_id)
        item.quantity = quant
        item.save()
        
        return Response({"details":"quantity saved"}, status=status.HTTP_200_OK)
    
    def delete(self, request, format=None):
        user = request.user
        item_id = request.GET.get('item_id')
        
        item = CartItem.objects.get(pk = item_id)
        item.delete()
        
        return Response({"details":"item deleted"}, status=status.HTTP_200_OK)
    
class CreateOrderView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def post(self, request, format=None):
        user = request.user
        cart_items = request.data.get('cart_items', [])
        presc = request.data.get('presc', None)
        payment_method = request.data.get('payment_method', 'ON_SITE')
        
        if len(cart_items) < 1:
            return Response({"detaiks": "No items Provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        items = CartItem.objects.filter(pk__in = cart_items)
        total_price = 0
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    customer = user,
                    channel = Order.Channel.ONLINE,
                    status = Order.Status.ORDER_CREATED, #see changes later
                    total_amount = 0,
                    created_at = timezone.now(),
                    updated_at = timezone.now(),
                )
                for item in items:
                    batch = ProductBatch.objects.filter(product = item.product).order_by('expiry_date')
                    batch = batch.filter(stock_qty__gt = item.quantity)
                    batch = batch.filter(expiry_date__gt = timezone.now()).first()
                    orditem = OrderItem.objects.create(
                        order = order,
                        batch = batch,
                        product = item.product,
                        quantity = item.quantity,
                        price_at_purchase = item.product.price,
                    )
                    
                    batch.stock_qty -= item.quantity
                    batch.save()
                    
                    StockMovement.objects.create(
                        batch=batch,
                        movement_type=StockMovement.MovementType.SALE,
                        created_at=timezone.now(),
                        quantity=-item.quantity,  
                        notes=f"Order Creation: {order.id}"
                    )
                    
                    total_price += item.quantity * item.product.price
                    
                    item.delete()
                
                order.total_amount = total_price
                order.save()
                
                if payment_method != 'ON_SITE':
                    # online payment simulator
                    payment_success = random.choices([True, False], weights=[90, 10], k=1)[0]
                    
                    pay_record = Payment.objects.create(
                        order=order,
                        payment_method=f"MOCK_GATEWAY_{payment_method}",
                        amount=total_price,
                        transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}"
                    )
                    
                    if payment_success:

                        pay_record.status = Payment.Status.SUCCESSFUL
                        pay_record.paid_at = timezone.now()
                        pay_record.save()
                        

                        order.status = Order.Status.PAID
                        order.save()
                    else:

                        pay_record.status = Payment.Status.FAILED
                        pay_record.save()
                        

                        raise ValueError("Mock Payment Gateway: Transaction declined by issuing bank (Simulated Insufficient Funds).")
                
            return Response(
                {
                    "details": "Order Created.",
                    "transaction_id": order.id,
                },
                status=status.HTTP_201_CREATED,
            )   
                     
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "Internal Database Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )    

class OrderListView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        user = request.user
        
        ord = Order.objects.filter(customer = user).order_by('-created_at')
        
        serial = OrderDetailedSerializer(ord, many = True)
        return Response(serial.data)
    
class OrderManageListView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        user = request.user
        
        ord = Order.objects.filter(Q(status = Order.Status.ORDER_CREATED) | Q(status = Order.Status.PAID)).order_by('-created_at')
        ord1 = Order.objects.filter(status = Order.Status.PREPARING).order_by('-created_at')
        
        serial_created = OrderListSerializer(ord, many=True)
        serial_prep = OrderListSerializer(ord1, many=True)
        
        return Response({"created" : serial_created.data, "prepare" : serial_prep.data})
    
class BatchActionsView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    
    def put(self, request, format=None):
        user = request.user
        id = request.GET.get('id')
        batch_number = request.GET.get('batch_number')
        supplier = request.GET.get('supplier')
        expiry_date = request.GET.get('expiry_date')
        stock_qty = request.GET.get('stock_qty')
        type = request.GET.get('type')
        
        batch = ProductBatch.objects.get(pk = id)
        try:
            with transaction.atomic():
                tmp_quant = int(stock_qty) - batch.stock_qty
                batch.batch_number = batch_number if batch_number else batch.batch_number
                batch.supplier_id = supplier if supplier else batch.supplier_id
                batch.expiry_date = expiry_date if expiry_date else batch.expiry_date
                batch.stock_qty = stock_qty if stock_qty else 0
                batch.save()
                
                stock = StockMovement.objects.create(
                    batch = batch,
                    movement_type = type,
                    created_at = timezone.now(),
                    quantity = tmp_quant,
                    notes = type
                )
                
            return Response({'details' : 'batch edited'}, status=status.HTTP_200_OK)
        
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Internal Database Error {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
    def post(self, request, format=None):
        user = request.user
        id = request.data.get('id', '')
        product_id = request.data.get('product_id')
        batch_number = request.data.get('batch_number')
        supplier = request.data.get('supplier')
        expiry_date = request.data.get('expiry_date')
        stock_qty = request.data.get('stock_qty', 1)
        
        try:
            with transaction.atomic():
                batch = ProductBatch.objects.create(
                    product_id = product_id,
                    supplier_id = supplier,
                    batch_number = batch_number,
                    expiry_date = expiry_date,
                    stock_qty = stock_qty,
                    created_at = timezone.now()
                )
                
                stock = StockMovement.objects.create(
                    batch = batch,
                    movement_type = StockMovement.MovementType.PURCHASE,
                    created_at = timezone.now(),
                    quantity = stock_qty,
                    notes = StockMovement.MovementType.PURCHASE
                )
                
            return Response({'details' : 'batch created'}, status=status.HTTP_201_CREATED)
        
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Internal Database Error {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )    
        
    def delete(self, request, format=None):
        user = request.user
        id = request.GET.get('id')
        if not id:
            return Response({"error": 'no id'}, status=status.HTTP_400_BAD_REQUEST)
        batch = ProductBatch.objects.get(pk = id)
        with transaction.atomic():
            stock = StockMovement.objects.create(
                    batch = batch,
                    movement_type = StockMovement.MovementType.DELETED,
                    created_at = timezone.now(),
                    quantity = batch.stock_qty,
                    notes = f"delete stock {batch.batch_number}"
                )
            batch.delete()
        return Response({'details' : 'batch deleted'}, status=status.HTTP_200_OK)
    
class ProductActivateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, format=None):
        user = request.user
        id = request.GET.get('id')
        is_active = request.GET.get('is_active')
        
        prod = Product.objects.get(pk = id)
        prod.is_active = is_active == 'true'
        prod.save()
        
        return Response({'details': 'Product updated successfully'}, status=status.HTTP_200_OK)
        
class ProductActionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def put(self, request, format=None):
        product_id = request.data.get('id')
        if not product_id:
            return Response({"error": "Product ID is required for updates."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            prod = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        sku = request.data.get('sku')
        name = request.data.get('name')
        generic_name = request.data.get('generic_name')
        category_id = request.data.get('category')
        dosage_form = request.data.get('dosage_form')
        strength = request.data.get('strength')
        price = request.data.get('price')
        minimum_stock = request.data.get('minimum_stock')
        description = request.data.get('description')
        image_file = request.FILES.get('image')
        
        requires_prescription_raw = request.data.get('requires_prescription')
        try:
            with transaction.atomic():
                prod.sku = sku if sku is not None else prod.sku
                prod.name = name if name is not None else prod.name
                prod.generic_name = generic_name if generic_name != "" else "-"
                prod.dosage_form = dosage_form if dosage_form is not None else prod.dosage_form
                prod.strength = strength if strength is not None else prod.strength
                prod.description = description if description is not None else prod.description
                
                if category_id:
                    prod.category_id = int(category_id)

                if price is not None:
                    prod.price = float(price)
                if minimum_stock is not None:
                    prod.minimum_stock = int(minimum_stock)
                    
                if requires_prescription_raw is not None:
                    prod.requires_prescription = requires_prescription_raw == 'true'
                    
                if image_file:
                    prod.image = image_file
                    
                prod.save()
        except Exception as e:
            return Response(
                {"error": f"Internal Database Error {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
        return Response({'details': 'Product updated successfully'}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        sku = request.data.get('sku')
        name = request.data.get('name')
        category_id = request.data.get('category')
        price = request.data.get('price')
        
        if not all([sku, name, category_id, price]):
            return Response({"error": "SKU, Name, Category, and Price are required."}, status=status.HTTP_400_BAD_REQUEST)
            
        generic_name = request.data.get('generic_name')
        dosage_form = request.data.get('dosage_form')
        strength = request.data.get('strength')
        minimum_stock = request.data.get('minimum_stock', 5)
        description = request.data.get('description')
        image_file = request.data.get('image')
        
        is_active = request.data.get('is_active', 'true') == 'true'
        requires_prescription = request.data.get('requires_prescription') == 'true'

        with transaction.atomic():
            new_product = Product.objects.create(
                sku=sku,
                name=name,
                generic_name=generic_name if generic_name != "" else None,
                category_id=int(category_id),
                dosage_form=dosage_form,
                strength=strength,
                price=float(price),
                minimum_stock=int(minimum_stock),
                description=description,
                is_active=is_active,
                requires_prescription=requires_prescription,
                image=image_file
            )
            
        return Response({'details': 'Product created successfully', 'id': new_product.id}, status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        product_id = request.GET.get('id') or request.data.get('id')
        
        if not product_id:
            return Response({"error": "Product ID is required for deletion."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            prod = Product.objects.get(pk=product_id)
        
            prod.delete()
            
            return Response({'details': 'Product removed successfully'}, status=status.HTTP_200_OK)
            
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
class OrderItemsListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, id, format=None):
        user = request.user
        
        ord = Order.objects.get(pk = id)
        items = OrderItem.objects.filter(order = ord).order_by("id")
        
        serial = OrderItemComplicatedSerializer(items, many=True)
        return Response(serial.data)

class PrepReadyOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, id, format=None):
        user = request.user
        stat = request.GET.get("stat")
        
        ord = Order.objects.get(pk = id)
        items = OrderItem.objects.filter(order = ord)
        
        if stat == Order.Status.READY:
            for item in items:
                if item.batch is None:
                    return Response({"details": "all batches havent been picked"}, status=status.HTTP_400_BAD_REQUEST)

        ord.status = stat if stat else Order.Status.PREPARING
        ord.save()
        return Response({'details': 'Product removed successfully'}, status=status.HTTP_200_OK)
    
class setOrderItemBatch(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, format=None):
        user = request.user
        id = request.GET.get("id")
        batch = request.GET.get("batch")
        
        item = OrderItem.objects.get(pk = id)
        batch = ProductBatch.objects.get(pk = batch)
        
        item.batch = batch
        item.save()
        return Response({'details': 'Product removed successfully'}, status=status.HTTP_200_OK)
    
class cashierOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        user = request.user
        id = request.GET.get('id')
        
        if not id:
            return Response({"error": "Product ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        ord = Order.objects.get(pk = id)
        usr = User.objects.get(pk = ord.customer.id)
        cust = CustomerProfile.objects.get(user = usr)
        
        serial = OrderDetailedSerializer(ord)
        serusr = UserSerializer(usr)
        sercust = CustomerProfileSerializer(cust)
        return Response({"data" : serial.data,
                         "user": serusr.data,
                         "profile": sercust.data})
        
        
class OrderOnSItePayView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, id, format=None):
        try:
            ord = Order.objects.get(pk=id)
        except Order.DoesNotExist:
            return Response({"error": "Order profile not found."}, status=status.HTTP_404_NOT_FOUND)
        if ord.status == Order.Status.COMPLETED:
            return Response({"error": "This order has already been finalized and completed."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                pay_record = Payment.objects.create(
                        order=ord,
                        payment_method="Cashier counter",
                        amount=ord.total_amount,
                        transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
                        status = Payment.Status.SUCCESSFUL,
                        paid_at = timezone.now()
                    )

                ord.status = Order.Status.PAID
                ord.updated_at = timezone.now()
                ord.save()
                
            return Response({'details': 'Order Paid successfully.'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": f"Internal Database Transaction Error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )  
              
class OrderCompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, id, format=None):
        try:
            ord = Order.objects.get(pk=id)
        except Order.DoesNotExist:
            return Response({"error": "Order profile not found."}, status=status.HTTP_404_NOT_FOUND)
        if ord.status == Order.Status.COMPLETED:
            return Response({"error": "This order has already been finalized and completed."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                    
                ord.status = Order.Status.COMPLETED
                ord.updated_at = timezone.now()
                ord.save()
                
            return Response({'details': 'Order Paid successfully.'}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": f"Internal Database Transaction Error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )    